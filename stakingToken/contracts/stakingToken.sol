pragma solidity 0.8.7;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract StakingCoin is ERC20, ERC20Burnable, ReentrancyGuard {
    
    struct Staker {
        // внесенный депозит
        uint256 deposited;
        // время через которое можно обратиться к функциям стейкинга контракта
        uint256 timeOfAccess;
        // накопленное количество кешбека
        uint256 rewards;
        // время через которое разрешен вывод кешбека
        uint256 timeOfWithdraw;
        // время последнего обращения пользователя к контракту
        uint256 timeOfLastUpdate;
    }

    event Withdraw(address indexed sender, uint256 indexed amount);
    event Deposit(address indexed sender, uint256 indexed coins);
    event StakeInfo(uint256 indexed stake, uint256 indexed rewards);
    event TimeInfo(uint256 indexed access, uint256 indexed withdraw);
    event WithdrawAll(address indexed sender,uint256 indexed totalCoins);

    mapping(address => Staker) internal stakers;
    // через час можно обратиться к контракту
    uint256 private intervalTimeAccess = 1 hours;
    // черещ 24 часа можно вывести монеты и реварды или только реварды 
    uint256 private intervalTimeWithdraw = 1 days;
    // минтим токены для владельца контракта для демонстрации стейкинга
    constructor() ERC20("StakingCoin", "SCT") {
        _mint(msg.sender,1000000000000);
    }
    // проверяем разрешено ли пользователю доступ к контракту по временому интервалу 1 час
    modifier preChecksTimeToAccess {
        if (stakers[msg.sender].timeOfAccess != 0) {
            require(
                block.timestamp >= stakers[msg.sender].timeOfAccess,
                "Please wait time for allow access to contract"
            );
        }
        _;
    }
    // проверяем разрешено ли пользователю выводить монеты с ревардами или только реварды по временому интервалу 24 часа
    modifier preChecksTimeToWithdraw {
        if (stakers[msg.sender].timeOfWithdraw != 0) {
            require(
                block.timestamp >= stakers[msg.sender].timeOfWithdraw,
                "Please wait time for allow access to withdraw"
            );
        }
        _;
    }
    // допустимый ли баланс у пользователя для внесения в стейкинг
    modifier preChecksBalance(address _user,uint256 _coins) {
        require(
            balanceOf(_user) >= _coins,
            "Can't stake more than you own"
        );
        _;
    }
    // проверка пользователь вносил депозит в стейкинг или есть ли пользователь в интерфейсе стейкинга
    modifier checkIsUserExists(address _user) {
        require(stakers[_user].timeOfAccess != 0 || stakers[_user].timeOfWithdraw != 0,"user not exists");
        _;
    }
    // вычисляются реварды сл образом: депозит умножается на последнее время обращения пользователя к контракту которое из секунд преобразовано в часы и делится на 10, где 10 это проценты
    function calculateRewards(address _user) private returns (uint256) {
        uint256 timeOfLastUpdate = stakers[_user].timeOfLastUpdate;
        uint256 deposited = stakers[_user].deposited;
        return ((deposited*(block.timestamp-timeOfLastUpdate))/intervalTimeAccess)/10;
    }

    // функция взноса депозита в стейкинг
    function depositStaking(uint256 _coins) external 
    nonReentrant 
    preChecksBalance(msg.sender,_coins)
    preChecksTimeToAccess {
        if (stakers[msg.sender].rewards != 0) { // реварды будут капать только после сл обращения к контракту
            stakers[msg.sender].rewards += calculateRewards(msg.sender);
        }
        stakers[msg.sender].deposited += _coins; // аккумулируем депозит
        stakers[msg.sender].timeOfAccess = block.timestamp+intervalTimeAccess; // сохраняем сл время доступа ко всему интерфейсу стейкинга 
        stakers[msg.sender].timeOfWithdraw = block.timestamp+intervalTimeWithdraw; // сохраняем сл время доступа на вывод ревардов или монет с ревардами
        stakers[msg.sender].timeOfLastUpdate = block.timestamp; // сохраняем последнее время обращения пользователя к контракту
        _burn(msg.sender, _coins); // сжигаем токены
        emit Deposit(msg.sender,_coins); // сообщаем фронтенду об успешном совершение операции внесение депозита в стейкинг
    }

    // функция получения информации о стейкинге, а именно количество внесенных монет, то есть размер депозита и количество ревардов + вычисленные текущие накапанные реварды
    function getStakeInfo(address _user) public
    preChecksTimeToAccess
    checkIsUserExists(_user) {
        uint256 _stake = stakers[_user].deposited; // получаем депозит
        uint256 _rewards = calculateRewards(_user) + stakers[_user].rewards; // вычисляем текущий реварды плюс накопленные за все время для запрошенного юзера
        stakers[msg.sender].rewards += calculateRewards(msg.sender); // сохрание текущих ревардов как кешбек за операцию
        stakers[msg.sender].timeOfAccess = block.timestamp+intervalTimeAccess; // фиксация временных интервалов для контроля доступа к интерфейсу стейкинга контракта 
        stakers[msg.sender].timeOfLastUpdate = block.timestamp;
        emit StakeInfo(_stake,_rewards); // сообщаем фронту информацию
    }

    // функция вывода ревардов из стейкинга
    function withdrawRewards(uint256 _amount) external 
    nonReentrant
    preChecksTimeToAccess
    preChecksTimeToWithdraw
    checkIsUserExists(msg.sender) {
        require(stakers[msg.sender].rewards >= _amount,"amount greater then rewards"); // проверка того чтобы amount не был больше ревардов
        stakers[msg.sender].rewards -= _amount; // уменшаем реварды на указанный amount
        stakers[msg.sender].rewards += calculateRewards(msg.sender); // аккумулируем новые полученные реварды за операцию вывода
        stakers[msg.sender].timeOfAccess = block.timestamp+intervalTimeAccess; // фиксация временных интервалов для контроля доступа к интерфейсу стейкинга контракта
        stakers[msg.sender].timeOfWithdraw = block.timestamp+intervalTimeWithdraw;
        stakers[msg.sender].timeOfLastUpdate = block.timestamp;
        _mint(msg.sender, _amount); // чеканим новые токены из накопленых ревардов
        emit Withdraw(msg.sender, _amount); // сообщаем фронту об успешной операции вывода ревардов
    }

    
    function withdrawAll() external 
    nonReentrant
    preChecksTimeToAccess
    preChecksTimeToWithdraw
    checkIsUserExists(msg.sender) {
        uint256 rewards = stakers[msg.sender].rewards + calculateRewards(msg.sender); // получаем реварды за все время существования депозита в стейкинге
        uint256 deposit = stakers[msg.sender].deposited; // получаем депозит
        uint256 totalMint = rewards + deposit; // получаем полную сумму из ревардов и депозита
        stakers[msg.sender].rewards = 0; // данная операция не имеет получения ревардов
        stakers[msg.sender].deposited = 0; // депозит весь выведится из стейкинга, поэтому он сбрасывается в ноль
        stakers[msg.sender].timeOfAccess = block.timestamp+intervalTimeAccess; // фиксация временных интервалов для контроля доступа к интерфейсу стейкинга контракта
        stakers[msg.sender].timeOfWithdraw = block.timestamp+intervalTimeWithdraw;
        stakers[msg.sender].timeOfLastUpdate = block.timestamp;
        _mint(msg.sender, totalMint); // чеканка токенов
        emit WithdrawAll(msg.sender, totalMint); // сообщаем фронту об успешной операции вывода всего из стейкинга
    }

    // возвращает остаточное время в секундах, когда пользователь может обратиться ко всему интерфейсу стейкинга или к интерфейсу стейкинга вывода
    function getTimeAccessInfo() public checkIsUserExists(msg.sender) returns(uint256,uint256) {
        uint256 delta_access;
        uint256 delta_withdraw;
        unchecked {
            delta_access = stakers[msg.sender].timeOfAccess - block.timestamp;
            delta_withdraw = stakers[msg.sender].timeOfWithdraw - block.timestamp;
        }
        if (block.timestamp >= stakers[msg.sender].timeOfAccess){
            delta_access = 0;
        }
        if (block.timestamp >= stakers[msg.sender].timeOfWithdraw) {
            delta_withdraw = 0;
        } 
        emit TimeInfo(delta_access,delta_withdraw);
    }
}
