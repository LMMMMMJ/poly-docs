{
  description = "Polymarket API documentation mirror";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils, ... }:
    utils.lib.eachSystem [ "aarch64-linux" "x86_64-linux" "aarch64-darwin" "x86_64-darwin" ] (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in {
        devShells.default = pkgs.callPackage ./pkgs/dev-shell { };

        packages = {
          fetch-docs = pkgs.callPackage ./pkgs/fetch-docs { };
          default = pkgs.callPackage ./pkgs/fetch-docs { };
        };
      });
}
