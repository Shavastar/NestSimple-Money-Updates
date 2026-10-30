# NestSimple Money Updates

This repository hosts program update packages and release notes only. Household databases, personal records, profiles and passwords are never uploaded.

## Install v1.0.113

If v1.0.112 is installed, download [the v1.0.113 package](packages/NestSimple-Money-v1.0.113.nsmupdate), open NestSimple Money, choose **Install Update** below **Testing**, and select the downloaded file. Review it and choose **Apply Update and Restart**.

From v1.0.113, **Install Update** checks this repository, displays the latest version and numbered changes, and downloads the package for review. **Choose Update File** remains available for manually downloaded files.

The app checks package size, SHA256, allowed paths and installed-file compatibility. Program files are backed up before replacement, and household data and profiles are preserved. GitHub account security controls who may publish updates; checksums detect download damage and do not constitute a code-signing certificate.

## Publishing future updates

Add the versioned .nsmupdate file under packages/, then update latest.json with the version, public raw URL, exact byte size, SHA256 and numbered change strings. Publish the package and feed in the same commit so the feed never advertises a missing package. Preserve earlier packages. Do not put credentials or household data in this repository.
