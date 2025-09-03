{
  description = "A Nix-flake-based Python development environment";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    systems.url = "github:nix-systems/default";
  };

  outputs =
    {
      self,
      nixpkgs,
      systems,
      ...
    }:
    let
      inherit (nixpkgs) lib;

      eachSystem = lib.genAttrs (import systems);

      argsForEach = eachSystem (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
          pypkgs = pkgs.python313Packages;
        in
        {
          inherit system pkgs pypkgs;
        }
      );
    in
    {
      packages = lib.mapAttrs (system: args: {
        default = args.pypkgs.buildPythonApplication {
          pname = "ticman";
          version = "0.1.0";
          pyproject = true;
          src = ./.;
          build-system = [ args.pypkgs.setuptools ];
        };
      }) argsForEach;

      devShells = lib.mapAttrs (system: args: {
        default = args.pkgs.mkShell {
          venvDir = ".venv";
          packages = [ args.pypkgs.venvShellHook ];
        };
      }) argsForEach;
    };
}
