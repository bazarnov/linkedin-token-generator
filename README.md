### First Steps
1. Clone this project using `code > download as zip` or simply follow the instructions inside `code` section.
2. Open the folder with cloned project and follow the `Build` instructions.

### Build
Build the latest Docker image from local folder:
```
docker build . --no-cache -t linkedin-token-generator
```
Build the latest Docker using github link directly:
```
docker build https://github.com/bazarnov/linkedin-token-generator.git#main --no-cache -t linkedin-token-generator
```

### Create your config file
1. Go to `/linkedin_token_generator` folder
2. Create folder named `secrets`
3. Use the `../linkedin_token/samples/config.json` to create your own `config.json` file with your credentials.
4. Put the newly created `config.json` into the `secrets` folder from `step 2`.

### Run
Open `/linkedin_token_generator` folder. use the following command in Terminal to run the docker container:

```
docker run --rm -v $(pwd)/secrets:/secrets linkedin-token-generator generate --config /secrets/config.json
```

### Build and Run
You can build and run with one command in the terminal, before this, make sure you've followed all the steps from `create your config file`:

```
docker build https://github.com/bazarnov/linkedin-token-generator.git -t linkedin-token-generator \
    && docker run --rm -v $(pwd)/secrets:/secrets linkedin-token-generator generate --config /secrets/config.json
```

### Typical Output
You should now has the similar output to this:
```
{'scopes': ['r_emailaddress', 'r_liteprofile'], 'access_token': 'AQVzJ8Ju_----------------------L2hTBgLvcL_FuQ', 'expires_in': 5183999}
```
### Using the Output
Now you should be able to use your `'access_token'` value for making authenticated requests to LinkedIn Ads/Marketing API.
More information: [HERE](https://docs.microsoft.com/en-us/linkedin/marketing/getting-started)

#### NOTE: The `'access_token'` is valid for 2 months, after that, you must generate the new one.