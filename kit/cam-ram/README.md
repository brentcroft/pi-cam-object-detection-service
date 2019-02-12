The default value for *CURRENT_IMAGE_STORE* is **./cam-ram**.

The current image, maybe a detection file, and a boxed image will be continually rewritten into *CURRENT_IMAGE_STORE* 
so *CURRENT_IMAGE_STORE* is expected to be mounted as a RAM drive.

Every time the HTTP file server starts, it copies every file from **./site** (i.e. "index.html") into *CURRENT_IMAGE_STORE*.