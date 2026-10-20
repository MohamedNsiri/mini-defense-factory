# Observer: Nmap + Nuclei. Templates are baked at BUILD time (Internet available)
# so the container works offline on the isolated DMZ network.
FROM projectdiscovery/nuclei:latest
RUN apk add --no-cache nmap nmap-scripts curl bash
RUN nuclei -update-templates || true
ENTRYPOINT ["sleep", "infinity"]
