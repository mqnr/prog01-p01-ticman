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

      pkgsForEach = eachSystem (
        system:
        import nixpkgs {
          localSystem.system = system;
          overlays = [ self.overlays.default ];
        }
      );
    in
    {
      overlays.default = self: super: { pypkgs = super.python313Packages; };

      packages = lib.mapAttrs (system: pkgs: {
        default = pkgs.pypkgs.buildPythonApplication {
          pname = "ticman";
          version = "0.1.0";
          pyproject = true;
          src = ./.;
          build-system = [ pkgs.pypkgs.setuptools ];
        };
      }) pkgsForEach;

      devShells = lib.mapAttrs (system: pkgs: {
        default = pkgs.mkShell {
          venvDir = ".venv";
          packages = [ pkgs.pypkgs.venvShellHook ];
        };
      }) pkgsForEach;
    };
}
