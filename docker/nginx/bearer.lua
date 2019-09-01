local jwt = require "resty.jwt"

-- first try to find JWT token as url parameter e.g. ?token=BLAH
local token = ngx.var.arg_token

-- next try to find JWT token as Cookie e.g. token=BLAH
if token == nil then
    token = ngx.var.cookie_token
end

-- try to find JWT token in Authorization header Bearer string
if token == nil then
    local auth_header = ngx.var.http_Authorization
    if auth_header then
        _, _, token = string.find(auth_header, "Bearer%s+(.+)")
    end
end

-- finally, if still no JWT token, kick out an error and exit
if token == nil then
    ngx.status = ngx.HTTP_UNAUTHORIZED
    ngx.header.content_type = "application/json; charset=utf-8"
    ngx.say('{"errors": {"detail": "Token not found.", "status_code": 401, "is_error": true}}')
    ngx.exit(ngx.HTTP_UNAUTHORIZED)
end

-- make sure to set and put "env JWT_SECRET;" in nginx.conf
local jwt_obj = jwt:verify(os.getenv("JWT_SECRET_KEY"), token, {})
if not jwt_obj["verified"] then
    ngx.status = ngx.HTTP_UNAUTHORIZED
    ngx.header.content_type = "application/json; charset=utf-8"
    ngx.say(os.getenv("JWT_SECRET_KEY"))
  --  ngx.say('{"errors": {"detail": "Token decode error.", "status_code": 401, "is_error": true}}')
    ngx.exit(ngx.HTTP_UNAUTHORIZED)
end

-- optionally set Authorization header Bearer token style regardless of how token received
-- if you want to forward it by setting your nginx.conf something like:
--     proxy_set_header Authorization $http_authorization;`
ngx.req.set_header("Authorization", "Bearer " .. token)
