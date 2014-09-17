/** @jsx React.DOM */
'use strict';


var React = require('react');

var webservices = require('./webservices');


var appconfig = global.appconfig;


function init() {
  var enabledModules = appconfig.enabledModules;
  if (enabledModules.auth) {
    var auth = require('./auth');
    auth.init(enabledModules.auth);
  }
  var jsModal = document.getElementById('js-modal');
  if (enabledModules.acceptCookiesModal) {
    var AcceptCookiesModal = require('./components/accept-cookies-modal');
    React.renderComponent(
      <AcceptCookiesModal actionUrlPath={enabledModules.acceptCookiesModal.actionUrlPath} />,
      jsModal
    );
  }
  else if (enabledModules.acceptCnilConditionsModal) {
    var AcceptCnilConditionsModal = require('./components/accept-cnil-conditions-modal');
    React.renderComponent(
      <AcceptCnilConditionsModal
        actionUrlPath={enabledModules.acceptCnilConditionsModal.actionUrlPath}
        termsUrlPath={enabledModules.acceptCnilConditionsModal.termsUrlPath}
      />,
      jsModal
    );

  }
  if ( ! enabledModules.acceptCookiesModal && ! enabledModules.acceptCnilConditionsModal) {
    if (enabledModules.disclaimer) {
      var disclaimer = require('./disclaimer');
      disclaimer.init(enabledModules.disclaimer);
    }
  }
  if (enabledModules.legislation) {
    var legislation = require('./legislation');
    legislation.init(enabledModules.legislation);
  }
  if (enabledModules.situationForm) {
    webservices.fetchCurrentLocaleMessages(messages => {
      var Simulator = require('./components/simulator'),
        mountNode = document.getElementById('simulator-container');
      React.renderComponent(<Simulator messages={messages} />, mountNode);
    });
  }
}

module.exports = {init: init};
