splash:on_request(function(request)
    request:set_proxy {
        host = "zproxy.lum-superproxy.io",
        port = 22225,
        username = splash.args.username,
        password = splash.args.password,
    }
end)
splash.images_enabled = false
splash:go(args.url)
return splash:html()