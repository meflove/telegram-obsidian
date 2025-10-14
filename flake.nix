{
  description = "Aquanter Bot";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = nixpkgs.legacyPackages.${system};

        python = pkgs.python313;

        pythonDeps = python.withPackages (
          ps:
            with ps; [
              pip
              ruff

              # Deps
              aiogram
            ]
        );

        nativeBuildInputs = [
          pythonDeps
        ];
      in {
        formatter = pkgs.alejandra;

        devShells.default = pkgs.mkShell {
          inherit nativeBuildInputs;

          packages = with pkgs; [
            pre-commit
          ];
        };
      }
    );
}
