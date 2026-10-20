FROM mini-defense-factory-web-front-01

RUN set -ex \
    && cat /usr/local/apache2/conf/httpd.conf \
        | tr '\n' '\r' \
        | perl -pe 's|<Directory />.*?</Directory>|<Directory />\n    AllowOverride none\n    Require all denied\n</Directory>|isg' \
        | tr '\r' '\n' \
        | tee /tmp/httpd.conf \
    && mv /tmp/httpd.conf /usr/local/apache2/conf/httpd.conf
