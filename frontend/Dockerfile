# build stage
FROM node:16-alpine as build-stage

WORKDIR /code/
ADD . /code/
RUN ls && cat package.json
RUN npm cache verify
RUN npm install
RUN npm run build


# production stage
FROM nginx:1.24-alpine as production-stage

RUN apk update
RUN apk upgrade
COPY nginx/nginx.conf /etc/nginx/nginx.conf
RUN rm -f /etc/nginx/conf.d/default.conf
COPY --from=build-stage /code/dist /dist/
RUN addgroup -S -g 1010 appuser
RUN adduser -S -u 1010 -G appuser appuser
RUN chown -R appuser:appuser /dist
RUN mkdir /var/run/nginx/
RUN touch /var/run/nginx/nginx.pid /var/run/nginx.pid
RUN chown -R appuser:appuser /var/run/nginx/nginx.pid /var/run/nginx.pid /etc/nginx /var/log/nginx /var/cache/nginx/
RUN find / -type f -perm /6000 -exec chmod a-s {} \; || true
USER appuser
EXPOSE 5173
CMD ["nginx", "-g", "daemon off;"]