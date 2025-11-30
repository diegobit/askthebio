

## Put extraction.md file to R2

### Copy files to r2

To copy files I recommend rclone:

```
rclone copy /path/to/crawl/out/* rclone_config_name:r2_bucket_name/path/to/dir/
```

Or just copy the resulting md somewhere on R2.

### Edit wrangler.toml

Create two buckets on R2, then edit `bucket_name` and `preview_bucket_name`

Edit `CONTEXT_KEY` with the path to the file.md




