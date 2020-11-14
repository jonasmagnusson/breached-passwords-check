# Breached Passwords Check

Check passwords from Keepass, Lastpass or Bitwarden against HaveIBeenPwned API. The passwords are hashed with SHA1 and sent to the HIBP API using a k-Anonymity model that allows a password to be searched for by partial hash.

## Install

Clone this repository and symlink it for easy access:

```bash
# Clone repository
git clone https://github.com/jonasmagnusson/breached-passwords-check.git /opt/breached-passwords-check

# Create executable symlink
ln -s /opt/breached-passwords-check/breached-passwords-check.py /usr/local/bin/breached-passwords-check
chmod +x /opt/breached-passwords-check/breached-passwords-check.py
```

### Basic Usage

Export your passwords from your password manager of choice to a CSV file. Only the password and name fields are used. Feed it to the script and enter the corresponding type, to get the fields name to match.

```bash
# Bitwarden
breached-passwords-check -f example-exports/bitwarden.csv -t bitwarden

# Lastpass
breached-passwords-check -f example-exports/lastpass.csv -t lastpass

# Keepass
breached-passwords-check -f example-exports/keepass.csv -t keepass
```

The output will look like this:

```bash
# Example output
2019-09-03 12:46:23 [INFO] Looking up passwords against Have I Been Pwned
2019-09-03 12:46:31 [INFO] Found breached password BadPassword for entry BreachedSite
2019-09-03 12:46:31 [INFO] Checked 3 passwords and 1 of them where breached
```
