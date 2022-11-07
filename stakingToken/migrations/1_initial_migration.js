const StakingCoin = artifacts.require("StakingCoin");

module.exports = function(deployer) {
  deployer.deploy(StakingCoin);
};
