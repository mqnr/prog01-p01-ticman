{
  description = "A Nix-flake-based Python development environment";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    systems.url = "github:nix-systems/default";
  };

  outputs =
    { nixpkgs, systems, ... }:
    let
      inherit (nixpkgs) lib;

      pypkgsFn = pkgs: { pypkgs = pkgs.python313Packages; };

      eachSystem = lib.genAttrs (import systems);

      pkgsForEach = eachSystem (system: import nixpkgs { localSystem.system = system; });
    in
    {
      packages = lib.mapAttrs (
        system: pkgs: with pypkgsFn pkgs; {
          default = pypkgs.buildPythonApplication {
            pname = "ticman";
            version = "0.1.0";
            pyproject = true;
            src = ./.;
            build-system = [ pypkgs.setuptools ];
          };
        }
      ) pkgsForEach;

      devShells = lib.mapAttrs (
        system: pkgs: with pypkgsFn pkgs; {
          default = pkgs.mkShell {
            venvDir = ".venv";
            packages = [ pypkgs.venvShellHook ];
          };
        }
      ) pkgsForEach;
    };
}
