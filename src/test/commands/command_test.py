def test_procfile_commands(procfile_command):
    print('\n --- Should return environment from command line argument equal to \'production\'')
    
    import re
    for arg in procfile_command:
        env = re.search('environment=(\w+)', arg)
        if env:
            assert env.group(1) == 'production'