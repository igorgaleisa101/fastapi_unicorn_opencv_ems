function wait_for_element(splash, css, maxwait)
    -- Wait until a selector matches an element
    -- in the page. Return an error if waited more
    -- than maxwait seconds.
    if maxwait == nil then
        maxwait = 10
    end
    return splash:wait_for_resume(string.format([[
            function main(splash) {
              var selector = '%s';
              var maxwait = %s;
              var end = Date.now() + maxwait*1000;

              function check() {
                if(document.querySelector(selector)) {
                  splash.resume('Element found');
                } else if(Date.now() >= end) {
                  var err = 'Timeout waiting for element';
                  splash.error(err + " " + selector);
                } else {
                  setTimeout(check, 100);
                }
              }
              check();
            }
          ]], css, maxwait))
end

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
wait_for_element(splash, ".track-statusbar")
return { cookies = splash:get_cookies() }