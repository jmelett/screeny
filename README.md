# screeny

`screeny` is a simple, minimalist Django-based web application designed to serve as an image backend for [Shottr](https://shottr.cc/). 

It enables users to upload, view, and download screenshots. Each uploaded screenshot is assigned a unique URL for easy access, and the application tracks the number of views for each image.

Primarily developed for deployment on [Divio Cloud](https://www.divio.com/), `screeny` should work on any environment that supports Docker, with Postgres for the database and S3 for storage.

Please note, `screeny` is a basic Minimum Viable Product (MVP) and may have additional features added in the future. While it works well for small-scale usage, it's not designed to scale for large-scale or high-traffic scenarios.
