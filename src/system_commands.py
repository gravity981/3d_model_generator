import subprocess


class SystemCommands:

    @staticmethod
    def generate_3d_model(output_dir: str, paramset: str, output_format: str, paramset_filepath: str,
                          openscad_model_filepath: str) -> bool:
        openscad_command = 'openscad -o {}/3d/{}.{} -p {} -P {} {}' \
            .format(output_dir, paramset, output_format, paramset_filepath, paramset, openscad_model_filepath)
        try:
            proc = subprocess.run(openscad_command.split(' '), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            proc.check_returncode()
        except Exception as e:
            print('error executing command: {}'.format(e))
            return False
        print('created \"{}/{}.{}\"'.format(output_dir, paramset, output_format))
        return True

    @staticmethod
    def generate_thumbnail(output_dir: str, paramset: str, paramset_filepath: str,
                           openscad_model_filepath: str) -> bool:
        openscad_command = 'openscad -o {}/thumbnail/{}.png -p {} -P {} --imgsize=192,192 {}' \
            .format(output_dir, paramset, paramset_filepath, paramset, openscad_model_filepath)
        try:
            proc = subprocess.run(openscad_command.split(' '), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            proc.check_returncode()
        except Exception as e:
            print('error executing command: {}'.format(e))
            return False
        print('created \"{}/{}.png\"'.format(output_dir, paramset))
        return True

    @staticmethod
    def generate_poster(columns: int, output_dir) -> bool:
        command = 'montage -tile {}x0 -geometry +0+0 {}/thumbnail/*.png {}/poster.png' \
            .format(columns, output_dir, output_dir)
        try:
            proc = subprocess.run(command.split(' '), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            proc.check_returncode()
        except Exception as e:
            print('error executing command: {}'.format(e))
            return False
        print('created \"{}/poster.png\"'.format(output_dir))
        return True
