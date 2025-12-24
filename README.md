# Options Pricing Tool

This application allows a user to select a stock, option type (call or put), strike price, and expiration date, and receive an option contract price calculated using the Black–Scholes model. The model price is displayed alongside the current market price of the same option for comparison.

The application is deployed as a Streamlit web app and is intended for educational use.

Live app: https://optionseducation.streamlit.app/

---

## Description

This project implements the Black–Scholes option pricing model to estimate the theoretical value of European options. Users can adjust contract parameters and observe how the model price compares to real market prices for the same option.

The goal is to build intuition around option pricing while also practicing applied Python development and deployment.

---

## Functionality

- Select an underlying stock
- Choose option type (call or put)
- Set strike price and expiration date
- Compute theoretical option price using Black–Scholes
- Compare model price to observed market price

---

## Model

- Black–Scholes pricing for European options
- Assumes constant volatility, risk-free rate, and no dividends
- Intended as a learning tool rather than a trading system

---

## Tech Stack

- Python
- Streamlit
- NumPy
- SciPy
- Market data APIs (for live option prices)
- Matplotlib / Plotly (for visualization, where applicable)

---

## Motivation

I built this project to better understand the Black–Scholes model and option pricing mechanics, while also gaining experience building and deploying a Python-based data application.

---

## Disclaimer

This tool is for educational purposes only and does not constitute financial or investment advice.

---

## License

MIT License
