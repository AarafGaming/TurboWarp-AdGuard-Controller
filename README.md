This is a small AdGuard controller that can turn on and off the protection and see Allowed, Blocked and Total DNS Queries.
Made with TurboWarp and Python
The Python acts as a bridge to connect to your server, this is used because if TurboWarp directly tries to connect to your AdGuard server, we get CORS errors. Python Talks to TurboWarp via a local webserver hosted on
port 9000, using the URL to transfer the server URL, username and password.
