import subprocess

def has_sudo_access():
    """
    We don't want to only check if the current process is run as root or not
    (so os.geteuid() == 0 can't be used, for example). What we actually want to
    check is whether the command we want to run can be run under sudo without
    requiring a password; than can happen either if the current process is run
    as root, OR if the password is cached (i.e. the user has alrady entered the
    credentials).

    The way to do this is by calling sudo without a password to see if it
    works, either by getting the returncode of that command by calling
    subprocess.call(), or by catching a Python exception if the command is not
    successful by using subprocess.check_call(). I prefer the second way 
    because exceptions in Python are cheap (performance-wise), this way is more
    Pythonic, and the exception can be tracked if some kind of error logging is
    used.
    """
    
    try:
        # The -n (non-interactive) sudo option prevents sudo from prompting the
        # user for a password. If a password is required for the command to
        # run, sudo will display an error message and exit.
        # 'true' does nothing but sudo can't be called alone
        subprocess.check_call(['sudo', '-n', 'true'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def command_output(command):
    """
    Run the command in a subprocess and returns the output
    """
    return subprocess.check_output(command, stderr=subprocess.STDOUT)

def sudo_command_output(command):
    """
    If sudo isn't available, just call the normal command_output().
    If it is available, call command_output() with sudo before the command.
    """
    if has_sudo_access():
        return command_output(['sudo'] + command)
    else:
        return command_output(command)

def networks_search():
    """
    Run iwlist and create a list of networks names using list comprehension
    (since it's very fast).
    """
    output = sudo_command_output(['iwlist', 'scan'])
    return [x.strip()[7:-1] for x in output.splitlines()
        if "ESSID" in x and len(x.strip())>8]

def battery_status():
    """
    Use acpi tool to get the status, capacity, and the remaining/until charged
    time of the battery.
    """
    # output usually looks something like "Battery 0: Discharging, 79%, 1:34:24
    # remaining"
    output = command_output(['acpi', '-b'])[:-1]
    output_list = output.split(" ")
    output_dict = {}

    # If the place in which the percentage should be is actually a number
    if output_list[3][:-2].isdigit():  
        # status is usually "Charging" or "Discharging"
        output_dict["status"] = output_list[2][:-1]
        output_dict["percent"] = output_list[3]
        # sometimes, acpi can't read the time
        if len(output_list) > 4:
            # if time is available, get rid of the ',' after percent
            output_dict["percent"] = output_list[3][:-1]
            output_dict["time"] = output_list[4]
            # time_info is usually "until charged" or "remaining"
            output_dict["time_info"] = " ".join(output_list[5:])  
            
    # Couldn't find the percentage, in case acpi didn't find a battery
    else:  
        output_dict["status"] = output

    return output_dict