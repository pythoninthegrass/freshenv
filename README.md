
[![Actions Status](https://github.com/raiyanyahya/freshenv/workflows/Build%20Test/badge.svg)](https://github.com/raiyanyahya/freshenv/actions) [![Actions Status](https://github.com/raiyanyahya/freshenv/workflows/Package%20Release/badge.svg)](https://github.com/raiyanyahya/freshenv/actions) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=raiyanyahya_freshenv&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=raiyanyahya_freshenv) [![CodeQL](https://github.com/raiyanyahya/freshenv/workflows/CodeQL/badge.svg)](https://github.com/raiyanyahya/freshenv/actions?query=workflow%3ACodeQL) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/d5e5d88f0cbf468b8fa6aaf820471139)](https://app.codacy.com/gh/raiyanyahya/freshenv?utm_source=github.com&utm_medium=referral&utm_content=raiyanyahya/freshenv&utm_campaign=Badge_Grade_Settings) [![](https://img.shields.io/badge/python-3.6+-blue.svg)]() [![](https://img.shields.io/github/license/raiyanyahya/freshenv.svg)]() [![PyPI version](https://badge.fury.io/py/freshenv.svg)](https://badge.fury.io/py/freshenv) [![PyPI download month](https://img.shields.io/pypi/dm/freshenv.svg)](https://pypi.python.org/pypi/freshenv/) [![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg) [![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg)


# Freshenv 
```freshenv``` is a  command line application to provision and manage local developer environments.

## Why?

This is a solution to a problem I have always had. I like my system to be clean, minimal and structured. 
It gets quite tricky to manage multiple projects on your on machine, projects tend to gather and are placed everywhere. 
Overtime managing system wide dependencies becomes a problem. It quite easy to mess up a system setting or to 
keep track of a package you wont need tomorrow. This is why i built ```freshenv```. It is a command line application
 which helps developers in running and managing completely isolated developer environments locally. 
It fetches and lets you run environment flavours in the form of docker containers
which are preconfigured with tools and packages developer needs everyday. Read about the usage below. 
I imagine it would help developers like me, its ```free and open source```. I hope you like it.


## Installation

Install the freshenv python package from pypi. You must have ```docker``` and ```python3.6+```  installed.

```console
  pip install freshenv
```
    
## Usage

```console
Usage: freshenv [OPTIONS] COMMAND [ARGS]...

  A cli to provision and manage local developer environments.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  provision  Provision a developer environment.
  remove     Remove a freshenv environment.
  start      Resume working in an environment.
  view       View local freshenv managed environments.
```

### Commands and Options

**```provision```**
```console
Usage: freshenv provision [OPTIONS]

  Provision a developer environment.

Options:
  -f, --flavour TEXT   The flavour of the environment.  [default: devenv]
  -c, --command TEXT   The command to execute at startup of environment.[default: zsh]
  -p, --ports INTEGER  List of ports to forward.  [default: 3000]
  -n, --name TEXT      Name of your environment.
  --help               Show this message and exit.
```


**```start```**
```console
Usage: freshenv start [OPTIONS]

  Resume working in an environment.

Options:
  -n, --name TEXT  Name of your environment to resume.  [required]
  --help           Show this message and exit.
```

**```remove```**
```console
Usage: freshenv remove [OPTIONS]

  Remove a freshenv environment.

Options:
  -n, --name TEXT  Name of the environment to remove.  [required]
  -f, --force      Force remove an environment.
  --help           Show this message and exit.
```

**```view```**
```console
Usage: freshenv view [OPTIONS]

  View local freshenv managed environments.

Options:
  --help  Show this message and exit.
```
## License

[MIT](https://choosealicense.com/licenses/mit/)


## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started. Please adhere to this project's `code of conduct`.


## Contact

Contact me at email raiyanyahyadeveloper@gmail.com.
