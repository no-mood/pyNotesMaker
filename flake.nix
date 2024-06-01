{
  description = "A Nix-flake-based Python development environment";

  inputs.nixpkgs.url = "https://flakehub.com/f/NixOS/nixpkgs/0.1.*.tar.gz";

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      devShells = forEachSupportedSystem ({ pkgs }: {
        default = pkgs.mkShell {
          venvDir = "venv";
          packages = with pkgs; [nodejs_22 python311 ] ++
            (with pkgs.python311Packages; [ 
              pip
              pynvim
              venvShellHook 

              numpy
              pytesseract
              pypdf2
              thefuzz
              openai-whisper
              #webvtt-py # not available in nixpkgs
            ]) ++ [
              # Other packages
              ffmpeg
            ];
            
         # shellHook = '' ''; # if set, venvShellHook doesn't work.
         postVenvCreation = ''
          pip install webvtt-py
         '';
         postShellHook = ''
        '';
          
        };
      });
    };
}
