# iup_server

This is the backend code for https://invisibleup.com. This does not include any of the content; I'd rather keep the history for that private.

Some neat features (so far!) include

- Automatic RSS generation
- Templating using Jinja
- Gopher support
- Nice schema for defining pages

...it's a little immature as of right now. I only update this as I need features for the site, or want to hack on this instead of other things. It's more of a fun pet project than anything serious. But it's open source. So hey.

## Installation

`iup_server` is a fairly vanilla Flask application. To run it, you'll need Python 3.6 or higher. This has been tested on Windows 10 and CentOS 7, although there's no reason it shouldn't work on any operating system that supports Python.

1. `pip install poetry`
2. `poetry install` or `poetry develop` for production and development configs, respectively
3. `poetry run wsgi.py`

This will start the internal Flask server at port 5000. The internal Flask server supports both HTTP and Gopher access.

The actual web server uses the nginx server with Flask set up as a proxy. An example nginx.conf is included in this repo.

To have gopher support on production, the internal Flask server is running in a seperate process with nginx.conf set to do a plain proxy pass. This is bad, but I don't have a lot of other options without significant work.

## Usage

To add content to the server, first you'll need to author some content. You can write in either HTML or Markdown, with Jinja syntax highlighting. You can also add any number of images, videos, or any other type of file.

Part templates are imported from content/templates. `_header.html` and `_footer.html` are automatically placed at the top and bottom of Markdown pages, but must be included manually for HTML pages. See the Jinja documentation for details on how to do that.

Once that's sorted out, you'll need to edit `content.toml`. This contains one entry for each page. Format it like so:

```toml
[section.page]
"title"=(Page Title)
"dir"=(location on web server page should appear)
"handler"=(one of MarkdownHandler for Markdown or TemplateHandler for HTML)
"series"=(Optional tag to be displayed on Articles index [not included in this repo])
"date"=(Optional last-modified date. Adding this will add the page to the RSS feed.)
```
Once that is updated, start or restart the server and enjoy your new content!

## FAQ

**Q: Why not just use Jekyll/Hugo?**
A: I want to do more with this than static site generators can really offer. It's not really at that point *yet* besides the Gopher support, but I'd rather start with a more flexible backend so I don't have to keep migrating.

**Q: Why'd you add Gopher support?**
A: I have rather strict HTTPS settings on the HTTP server, and the CSS doesn't work in older browsers. The Gopher server exists as an alternative for low-end or retro machines. That and I just like the Gopher community and the idea of a super lightweight protocol free from CSS and JavaScript and all that nonsense.

**Q: Why Python?**
A: I know Python. I considered Rust or Go, but Rust's ecosystem still seems a bit immature and while Go is easy to pick up, I wasn't confident enough to try that out. Plus Python has a lot of really neat web server stuff.

**Q: Why not NeoCities?**
A: I like the NeoCities community, but I don't like the interface for updating the site. It doesn't support any sort of SSGs unless I ran them locally, it's a little bit of a pain to maintain with the web GUI, and I wanted to run other stuff on my web server besides the site. I'm aware there is a CLI backend, and I do have WebDAV access, but I never had much luck with either of those.

## Contributing

I have literally no idea what I'm doing with this web server stuff, so if you want to give some assistance I'd gladly take it. I have no real rules right now, but if you have anything to contribute don't be afraid to send a pull request. I may or may not agree with the change, though. Keep in mind that this is the code for *my* webserver.

## TODO

### Dockerize this

This is high on my priority list, because currently my server is a bit of a pain to maintain and I can't easily install new web applications. If I could instead just have a more simplified setup where I just have to run one command, upload some files, and have that be that, then that'd be great. For now we don't have that though.

### Clean up Gopher

A thought is to make the Gopher server a seperate application entirely, and just have it read the same files as the Flask application. Perhaps this application could take the content/ directory and generate gohpermaps. The only advantage of doing this would be to use a better web server. I'd lose out on any backend interactivity though.

Another thought would be to add better support for front-end targets. Right now HTML is the primary target with Gopher and very rudimentary RSS sort of duct-taped on. If we could seperate the model from the view, we could be able to generate whatever sort of output we needed. That said besides Gopher and RSS and maaaaaybe JSON I can't think of much. Simplified HTML for retro browsers? I guess?

### Tagged File System

A radical idea I have is to throw out the old idea of each page having one set path, and instead just giving each page an ID and a set of tags. From some sort of sitemap page, we could give the user to filter by tags to find the content they want. The sections displayed at the top would just be shortcuts for each tag. I imagine each tag could have it's own introductory Markdown snippet, which would be especially helpful for the section landing pages. This would be neat to implement but a significant change from how things are

### Restartless updates

Right now I have to restart the iup_server process every time content.toml is changed, because it's loaded once at startup and never touched again. I'd like it to watch for changes in content.toml to know when to reload it automatically.
