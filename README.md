## First Steps
1. Install Docker on your system: [Instructions](https://www.docker.com/products/docker-desktop) select your OS.
2. Clone this project using `code > download as zip` or simply follow the instructions inside `code` section.
3. Open the folder with cloned project and follow the `Build` instructions.


## Build
Build the latest Docker image from local folder:
```
docker build . --no-cache -t linkedin-token-generator
```
Build the latest Docker using github link directly:
```
docker build https://github.com/bazarnov/linkedin-token-generator.git --no-cache -t linkedin-token-generator
```

## Create your config file
1. Go to `/linkedin_token_generator` folder
2. Create folder named `secrets`
3. Use the `../linkedin_token/samples/config.json` to create your own `config.json` file with your credentials.
4. Put the newly created `config.json` into the `secrets` folder from `step 2`.

## Run
Open `/linkedin_token_generator` folder. use the following command in Terminal to run the docker container:

```
docker run --rm -v $(pwd)/secrets:/secrets linkedin-token-generator generate --config /secrets/config.json
```

## Build and Run
You can build and run with one command in the terminal, before this, make sure you've followed all the steps from `create your config file`:

For MacOS X:
Open `Terminal` application and use this script:

Create prepared file structure and open the directory:
```
PATH_TO_DIR=$HOME/Desktop \
&& MAIN=linkedin_token \
&& mkdir $MAIN \
&& mkdir $PATH_TO_DIR/$MAIN/secrets/ \
&& touch $PATH_TO_DIR/$MAIN/secrets/config.json \
&& docker build https://github.com/bazarnov/linkedin-token-generator.git -t linkedin-token-generator \
&& echo "The folder $MAIN is created in $PATH_TO_DIR/$MAIN, docker container is build! Edit your config file" \
&& open $PATH_TO_DIR/$MAIN/secrets
```

After you've edited your `config.json`, please use the following command to generate your access_token:
```
PATH_TO_DIR=$HOME/Desktop \
&& MAIN=linkedin_token \
&& cd $PATH_TO_DIR/$MAIN \
&& docker run --rm -v $(pwd)/secrets:/secrets linkedin-token-generator generate --config /secrets/config.json
 ```

For Other OS:
The instructions for other OS are similar, there is no demand from users to do other instructions so far)

### Typical Output
You should now has the similar output to this:
```
{'scopes': ['r_emailaddress', 'r_liteprofile'], 'access_token': 'AQVzJ8Ju_----------------------L2hTBgLvcL_FuQ', 'expires_in': 5183999}
```
### Using the Output
Now you should be able to use your `'access_token'` value for making authenticated requests to LinkedIn Ads/Marketing API.
More information: [HERE](https://docs.microsoft.com/en-us/linkedin/marketing/getting-started)

#### NOTE: The `'access_token'` is valid for 2 months, after that, you must generate the new one.