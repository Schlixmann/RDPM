FROM fedora
MAINTAINER http://fedoraproject.org/wiki/Cloud

RUN dnf -y install ruby
RUN dnf -y install @buildsys-build @development-tools @c-development ruby-devel libxml2-devel libxslt-devel zlib-devel rasqal-devel raptor2-devel libicu-devel redis
RUN gem install cpee
RUN cpee new server
RUN cd server;./cpee start

EXPOSE 8080

CMD cpee ui