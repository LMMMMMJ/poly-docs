{ writeShellApplication, python3 }:

let
  python-env = python3.withPackages (p: with p; [
    requests
  ]);

  script = builtins.path {
    path = ../../scripts/fetch-docs.py;
    name = "fetch-docs.py";
  };

in writeShellApplication {
  name = "fetch-docs";

  runtimeInputs = [ python-env ];

  text = ''
    python ${script} "$@"
  '';
}
