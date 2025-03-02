# foosball_rating

### Poetry
```shell
# poetry -> requirements
poetry export --without-hashes --format=requirements.txt > requirements.txt
```



### Issue RSA private key + public key pair
*Чтобы не устанавливать openssl можно выполнить команды в контейнере и прокинуть с помощью volumes*
```shell
# Generate an RSA private key, of size 2048
openssl genrsa -out jwt-private.pem 2048
```

```shell
# Extract the public key from the key pair, which can be used in a certificate
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```