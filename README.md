My Library
===================

MyLibrary is an application for cataloging your books library.
The application is designed to help unite lovers of literature.
Find a rare book among users MyLibrary.

**It's server part - [Cement](https://builtoncement.com/)**

* server data backup
* cleaning up obsolete files and data
* sending firebase push messages

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-white.svg)](https://snapcraft.io/mylibrary)

### Backup db
```shell
mylibrary backup -t=db
```
Back up the database. You can specify a folder or ftp in the configuration file.


### Backup folder/dirs
```shell
mylibrary backup -t=tar
```
Back up the files or dirs in tar.gz. For compression use pigz (& tar) with multi-stream archive build capability.

### Clear db data
```shell
mylibrary cleaner -t=tokens
```
Clearing obsolete tokens from the database. Application specific.

```python
# find method in the project for change
def clear_old(cls, app):
```

### Clear db images relations
```shell
mylibrary cleaner -t=images
```
Clearing non-database images in the folder specified in the configuration file.

### Sending messages push firebase
```shell
mylibrary notification
```
Messaging google push firebase. Application specific. You need to build a request for a specific database.

```python
# find method in the project for change
def find_open(cls, app):
```

### Create reminder notification
```shell
# 15 days
mylibrary reminder -d=15

# 25 days
mylibrary reminder -d=25
```
Create reminder notification for 15 day and 25 day if user not open application. Application specific.

```python
# find Controller in the project for change
class Reminder(Controller):
```