import { useState, useEffect } from 'react'
import { Plus, Trash2, Wallet, TrendingDown, Calendar, Tag, CreditCard, Activity } from 'lucide-react'
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts'
import './index.css'

const API_URL = 'http://localhost:3001/api/expenses';

const CATEGORIES = [
  { id: 'food', label: 'Food & Dining', icon: '🍔', color: '#f59e0b' },
  { id: 'transport', label: 'Transportation', icon: '🚗', color: '#3b82f6' },
  { id: 'entertainment', label: 'Entertainment', icon: '🎬', color: '#8b5cf6' },
  { id: 'shopping', label: 'Shopping', icon: '🛍️', color: '#ec4899' },
  { id: 'bills', label: 'Bills & Utilities', icon: '📄', color: '#10b981' },
  { id: 'other', label: 'Other', icon: '✨', color: '#94a3b8' },
];

function App() {
  const [expenses, setExpenses] = useState([]);
  const [formData, setFormData] = useState({
    title: '',
    amount: '',
    category: 'food',
    date: new Date().toISOString().split('T')[0]
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchExpenses();
  }, []);

  const fetchExpenses = async () => {
    try {
      const res = await fetch(API_URL);
      const data = await res.json();
      setExpenses(data.data);
      setLoading(false);
    } catch (err) {
      console.error("Error fetching expenses", err);
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.title || !formData.amount || !formData.category || !formData.date) return;

    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      if (res.ok) {
        fetchExpenses();
        setFormData({ ...formData, title: '', amount: '' });
      }
    } catch (err) {
      console.error("Error adding expense", err);
    }
  };

  const handleDelete = async (id) => {
    try {
      const res = await fetch(`${API_URL}/${id}`, {
        method: 'DELETE',
      });
      if (res.ok) {
        fetchExpenses();
      }
    } catch (err) {
      console.error("Error deleting expense", err);
    }
  };

  const totalAmount = expenses.reduce((sum, item) => sum + parseFloat(item.amount), 0);

  // Group data for chart
  const categoryData = CATEGORIES.map(cat => {
    const value = expenses
      .filter(e => e.category === cat.id)
      .reduce((sum, e) => sum + parseFloat(e.amount), 0);
    return { name: cat.label, value, color: cat.color };
  }).filter(c => c.value > 0);

  return (
    <div className="app-container">
      <header className="animate-fade-in">
        <h1>
          <Wallet size={36} color="#3b82f6" /> 
          ExpenseTracker
        </h1>
        <div style={{display: 'flex', gap: '1rem'}}>
          <div className="glass-panel" style={{padding: '0.5rem 1rem', display: 'flex', alignItems: 'center', gap: '0.5rem', borderRadius: '30px'}}>
             <Activity size={18} color="#10b981" />
             <span style={{fontSize: '0.9rem', fontWeight: 500}}>System Online</span>
          </div>
        </div>
      </header>

      <main className="dashboard-grid">
        <section className="glass-panel expense-form animate-fade-in delay-1">
          <h2>Add New Expense</h2>
          <form onSubmit={handleSubmit} style={{display: 'flex', flexDirection: 'column', gap: '1.5rem'}}>
            <div className="form-group">
              <label><Tag size={14} style={{display:'inline', verticalAlign:'middle', marginRight: '4px'}}/> Title</label>
              <input 
                type="text" 
                name="title" 
                placeholder="e.g. Coffee, Groceries" 
                value={formData.title} 
                onChange={handleChange} 
                required 
              />
            </div>
            
            <div className="form-group">
              <label><CreditCard size={14} style={{display:'inline', verticalAlign:'middle', marginRight: '4px'}}/> Amount ($)</label>
              <input 
                type="number" 
                name="amount" 
                placeholder="0.00" 
                step="0.01" 
                value={formData.amount} 
                onChange={handleChange} 
                required 
              />
            </div>
            
            <div className="form-group">
              <label><TrendingDown size={14} style={{display:'inline', verticalAlign:'middle', marginRight: '4px'}}/> Category</label>
              <select name="category" value={formData.category} onChange={handleChange} required>
                {CATEGORIES.map(cat => (
                  <option key={cat.id} value={cat.id}>{cat.icon} {cat.label}</option>
                ))}
              </select>
            </div>
            
            <div className="form-group">
              <label><Calendar size={14} style={{display:'inline', verticalAlign:'middle', marginRight: '4px'}}/> Date</label>
              <input 
                type="date" 
                name="date" 
                value={formData.date} 
                onChange={handleChange} 
                required 
              />
            </div>
            
            <button type="submit" className="btn-primary" style={{marginTop: '0.5rem'}}>
              <Plus size={20} /> Add Expense
            </button>
          </form>

          {categoryData.length > 0 && (
            <div style={{marginTop: '2rem', height: '200px'}}>
              <h3 style={{fontSize: '1rem', color: 'var(--text-secondary)', marginBottom: '1rem', textAlign: 'center'}}>Spending by Category</h3>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={categoryData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {categoryData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} stroke="rgba(255,255,255,0.1)" />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{background: 'rgba(30, 41, 59, 0.9)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '10px'}}
                    itemStyle={{color: '#fff'}}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          )}
        </section>

        <section className="glass-panel expense-list-container animate-fade-in delay-2">
          <div className="expense-header">
            <div>
              <h2 style={{fontSize: '1.5rem', fontWeight: 600}}>Recent Expenses</h2>
              <p style={{color: 'var(--text-secondary)', fontSize: '0.9rem'}}>{expenses.length} transactions</p>
            </div>
            <div style={{textAlign: 'right'}}>
              <p style={{color: 'var(--text-secondary)', fontSize: '0.9rem', fontWeight: 500}}>Total Spent</p>
              <div className="total-amount">${totalAmount.toFixed(2)}</div>
            </div>
          </div>

          {loading ? (
            <div style={{textAlign: 'center', padding: '3rem', color: 'var(--text-secondary)'}}>Loading expenses...</div>
          ) : expenses.length === 0 ? (
            <div style={{textAlign: 'center', padding: '4rem 2rem', color: 'var(--text-secondary)', background: 'rgba(255,255,255,0.02)', borderRadius: '15px'}}>
              <Wallet size={48} style={{margin: '0 auto 1rem', opacity: 0.5}} />
              <h3 style={{fontSize: '1.2rem', color: 'var(--text-primary)', marginBottom: '0.5rem'}}>No expenses yet</h3>
              <p>Add your first expense using the form on the left.</p>
            </div>
          ) : (
            <div className="expense-list">
              {expenses.map((expense) => {
                const category = CATEGORIES.find(c => c.id === expense.category) || CATEGORIES[CATEGORIES.length - 1];
                return (
                  <div key={expense.id} className="expense-item">
                    <div className="expense-info">
                      <div className={`expense-icon icon-${category.id}`}>
                        {category.icon}
                      </div>
                      <div className="expense-details">
                        <h3>{expense.title}</h3>
                        <p>{category.label} • {new Date(expense.date).toLocaleDateString()}</p>
                      </div>
                    </div>
                    <div className="expense-actions">
                      <span className="expense-amount">-${parseFloat(expense.amount).toFixed(2)}</span>
                      <button className="btn-icon" onClick={() => handleDelete(expense.id)} title="Delete expense">
                        <Trash2 size={18} />
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

export default App
