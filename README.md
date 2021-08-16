#### Build
First, make sure you build the latest Docker image:
```
docker build . --no-cache -t linkedin-token-generator
```

#### Run
1. Go to `linkedin_token_generator` folder
2. Create folder named `secrets`
3. Use the `linkedin_token/samples/config.json` to create your own `config.json` file with your credentials.
4. Put the newly created `config.json` into the `secrets` folder from `step 2`.
5. Being in `linkedin_token_generator` folder, use the following command in Terminal to run the docker container:
    ```
    docker run --rm -v $(pwd)/secrets:/secrets linkedin-token-generator generate --config /secrets/config.json
    ```
You should now has the similar output to this:
```
{'scopes': ['r_emailaddress', 'r_liteprofile'], 'access_token': 'AQVzJ8Ju_----------------------wktfmApjamOTjlfo4Mv-L2hTBgLvcL_FuQ', 'expires_in': 5183999}
```
6. Use `'access_token'` value, to have the access to your LinkedIn Ads/Marketing API!

### NOTE: The `'access_token'` is valid for 2 months, after that, you must generate the new one.