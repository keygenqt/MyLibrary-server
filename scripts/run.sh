#! /bin/sh

# check default conf
if [ ! -f "$SNAP_USER_COMMON"/mylibrary.yml ]; then
    cp "$SNAP"/conf/mylibrary.yml "$SNAP_USER_COMMON"/mylibrary.yml
fi

# run app
"$SNAP"/usr/bin/python3 "$SNAP"/bin/mylibrary "$@"