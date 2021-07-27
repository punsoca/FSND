/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'mycafe101.us', // the auth0 domain prefix - i.e., the TENANT NAME 
    audience: 'http://mycafe101.com', // the audience set for the auth0 app
    clientId: '5seZoFclbovKST7UOWUBymm2CEk73oSt', // the client id generated for the auth0 app
    // the auth0 callback url must match the environment variable callbackURL
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
