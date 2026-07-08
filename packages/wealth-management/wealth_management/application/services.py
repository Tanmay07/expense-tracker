from typing import List, Dict
from wealth_management.domain.models import WealthProfile, Portfolio, Holding, InvestmentTransaction

class PortfolioService:
    def __init__(self):
        self.profiles: Dict[str, WealthProfile] = {}
        self.portfolios: Dict[str, Portfolio] = {}
        
    def get_or_create_profile(self, user_id: str) -> WealthProfile:
        for p in self.profiles.values():
            if p.user_id == user_id:
                return p
        profile = WealthProfile(user_id=user_id)
        self.profiles[profile.id] = profile
        return profile
        
    def create_portfolio(self, user_id: str, name: str, broker: str) -> Portfolio:
        profile = self.get_or_create_profile(user_id)
        portfolio = Portfolio(
            user_id=user_id,
            wealth_profile_id=profile.id,
            name=name,
            broker=broker
        )
        self.portfolios[portfolio.id] = portfolio
        return portfolio
        
    def get_portfolios(self, user_id: str) -> List[Portfolio]:
        return [p for p in self.portfolios.values() if p.user_id == user_id]
        
    def deposit_cash(self, portfolio_id: str, amount: float) -> Portfolio:
        portfolio = self.portfolios.get(portfolio_id)
        if not portfolio:
            raise ValueError("Portfolio not found")
        portfolio.cash_balance += amount
        return portfolio

class HoldingService:
    def __init__(self):
        self.holdings: Dict[str, Holding] = {}
        
    def get_or_create_holding(self, portfolio_id: str, asset_symbol: str, asset_class: str) -> Holding:
        for h in self.holdings.values():
            if h.portfolio_id == portfolio_id and h.asset_symbol == asset_symbol:
                return h
        holding = Holding(
            portfolio_id=portfolio_id,
            asset_symbol=asset_symbol,
            asset_class=asset_class,
            quantity=0.0,
            average_cost=0.0
        )
        self.holdings[holding.id] = holding
        return holding

class InvestmentTransactionService:
    def __init__(self, portfolio_svc: PortfolioService, holding_svc: HoldingService):
        self.transactions: Dict[str, InvestmentTransaction] = {}
        self.portfolio_svc = portfolio_svc
        self.holding_svc = holding_svc
        
    def execute_buy(self, portfolio_id: str, asset_symbol: str, asset_class: str, quantity: float, price: float) -> InvestmentTransaction:
        portfolio = self.portfolio_svc.portfolios.get(portfolio_id)
        if not portfolio:
            raise ValueError("Portfolio not found")
            
        total_cost = quantity * price
        if portfolio.cash_balance < total_cost:
            raise ValueError("Insufficient cash in portfolio")
            
        # Deduct cash
        portfolio.cash_balance -= total_cost
        
        # Update holding
        holding = self.holding_svc.get_or_create_holding(portfolio_id, asset_symbol, asset_class)
        
        # Calculate new average cost
        total_value = (holding.quantity * holding.average_cost) + total_cost
        holding.quantity += quantity
        holding.average_cost = total_value / holding.quantity
        
        # Record Transaction
        tx = InvestmentTransaction(
            portfolio_id=portfolio_id,
            holding_id=holding.id,
            transaction_type="BUY",
            asset_symbol=asset_symbol,
            quantity=quantity,
            price_per_unit=price,
            total_amount=total_cost
        )
        self.transactions[tx.id] = tx
        return tx
