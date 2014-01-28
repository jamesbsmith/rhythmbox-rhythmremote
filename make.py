# ------------------------------------------------------------------------------
# - Copyright (c) 2012 Christian Ertler.
# - All rights reserved. This program and the accompanying materials
# - are made available under the terms of the GNU Public License v3.0
# - which accompanies this distribution, and is available at
# - http://www.gnu.org/licenses/gpl.html
# - 
# - Contributors:
# -     Christian Ertler - initial API and implementation
# -     James B. Smith - add schema file and preferences dialog
# ------------------------------------------------------------------------------

import os, sys, subprocess, shutil

__plugin_dir = os.path.expanduser("~/.local/share/rhythmbox/plugins/")
__plugin_name = "RhythmRemote"
__schema_dir_local = os.path.expanduser("~/.local/glib-2.0/schemas/")
__schema_file = "org.gnome.rhythmbox.plugins.rhythmremote.gschema.xml"


def __cmd_exists(cmd):
    try:
        subprocess.call([cmd, '--version'])
    except OSError:
        print "%s not found on path" % myexec

def __unlink_project():
    if (os.path.lexists(__plugin_dir + __plugin_name.lower())):
        try:
            os.unlink(__plugin_dir + __plugin_name.lower())
        except:
            shutil.rmtree(__plugin_dir + __plugin_name.lower())

def __install():
    __unlink_project()
    shutil.copytree(os.path.abspath("."), __plugin_dir + __plugin_name.lower()) # TODO

def __run():
    __unlink_project()
    os.symlink(os.path.abspath("."), __plugin_dir + __plugin_name.lower())
    os.execvp("rhythmbox", ["rhythmbox", "-D", __plugin_name.lower()])

def __check_dependencies():
    try:
        import bottle
    except:
        print("You need to install bottle (pip install bottle or apt-get install python-bottle or ...)")
        exit(1)
    
    try:
        subprocess.call(["rhythmbox", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        print("Either Rhythmbox is not installed or not in your PATH environment variable.")
        print("Please install Rhythmbox properly to continue.")
        exit(1)

    try:
        subprocess.call(["which", "glib-compile-schemas"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        print("glib-compile-schemas not found")
        print("Please check your installation of glib2.")
        exit(1)

def __initialize_environment():
    if not os.path.exists(__plugin_dir):
        os.makedirs(__plugin_dir)
        print("Created Rhythmbox plugin-directory in: " + __plugin_dir)

def __initialize_schema_local():
    if not os.path.exists(__schema_dir_local):
        os.makedirs(__schema_dir_local)
        print("Created local schema directory in: " + __schema_dir_local)
    shutil.copy("gsettings.py.local", "gsettings.py")
    shutil.copy(__schema_file, __schema_dir_local)
    print("schema file " + __schema_file +  "copied to " + __schema_dir_local)

    try:
        subprocess.call(["glib-compile-schemas", __schema_dir_local], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("glib-compile-schemas compiled schema files in " + __schema_dir_local)
    except OSError:
        print("glib-compile-schemas failed to compile schema files in " + __schema_dir_local)
        exit(1)


if __name__ == "__main__":
    __check_dependencies()
    __initialize_environment()	
    __initialize_schema_local()

    if len(sys.argv) > 1 and sys.argv[1] == "install":
         __install()
    else:
         __run()
