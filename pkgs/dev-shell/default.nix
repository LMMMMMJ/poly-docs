{ mkShell, python3 }:

let
  python-env = python3.withPackages (p: with p; [
    requests
  ]);

in mkShell {
  name = "poly-docs";

  packages = [ python-env ];

  shellHook = ''
    echo "poly-docs dev shell"
    echo "Run: python scripts/fetch-docs.py [--dry-run] [--force]"
  '';
}
