import React, { useState, useEffect, useCallback } from "react";
import "./App.css";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

function App() {
	const [status, setStatus] = useState(null);
	const [history, setHistory] = useState([]);
	const [fundCatalog, setFundCatalog] = useState({});
	const [selectedFundId, setSelectedFundId] = useState("");
	const [message, setMessage] = useState("");
	const [error, setError] = useState("");

	const fetchData = useCallback(async () => {
		try {
			const [statusRes, catalogRes] = await Promise.all([
				fetch(`${API_URL}/funds/status-history`),
				fetch(`${API_URL}/funds/catalog`),
			]);

			if (!statusRes.ok || !catalogRes.ok) {
				throw new Error("Error al cargar los datos iniciales.");
			}

			const statusData = await statusRes.json();
			const catalogData = await catalogRes.json();

			setStatus(statusData.status);
			setHistory(statusData.history);
			setFundCatalog(catalogData);
		} catch (err) {
			setError(err.message);
		}
	}, []);

	useEffect(() => {
		fetchData();
	}, [fetchData]);

	const handleApiCall = async (action, fundId) => {
		setMessage("");
		setError("");
		try {
			const response = await fetch(`${API_URL}/funds/${action}`, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ fund_id: parseInt(fundId) }),
			});
			const data = await response.json();
			if (response.ok) {
				setMessage(data.message || `Operación ${action} exitosa`);
				fetchData(); // Recargar todos los datos
			} else {
				throw new Error(data.detail || `Error en la operación ${action}`);
			}
		} catch (err) {
			setError(err.message);
		}
	};

	const availableFundsToSubscribe = Object.entries(fundCatalog).filter(
		([id]) => !(status?.subscribed_funds && status.subscribed_funds[id])
	);

	return (
		<div className='App'>
			<header className='App-header'>
				<h1>Portal de Fondos</h1>
				{status && (
					<div className='status-card'>
						<h2>Mi Estado Actual</h2>
						<p>
							Saldo Disponible:{" "}
							<strong>
								${new Intl.NumberFormat("es-CO").format(status.balance)}
							</strong>
						</p>
						<h3>Mis Fondos</h3>
						{status.subscribed_funds &&
						Object.keys(status.subscribed_funds).length > 0 ? (
							<ul className='fund-list'>
								{Object.entries(status.subscribed_funds).map(([id, fund]) => (
									<li key={id}>
										<span>
											{fund.name} - Invertido: $
											{new Intl.NumberFormat("es-CO").format(fund.amount)}
										</span>
										<button
											className='cancel-btn'
											onClick={() => handleApiCall("cancel", id)}
										>
											Cancelar
										</button>
									</li>
								))}
							</ul>
						) : (
							<p>Aún no estás suscrito a ningún fondo.</p>
						)}
					</div>
				)}

				<div className='action-card'>
					<h2>Suscribir a un Nuevo Fondo</h2>
					<div className='subscribe-controls'>
						<select
							value={selectedFundId}
							onChange={(e) => setSelectedFundId(e.target.value)}
						>
							<option value=''>-- Seleccione un fondo --</option>
							{availableFundsToSubscribe.map(([id, fund]) => (
								<option key={id} value={id}>
									{fund.name}
								</option>
							))}
						</select>
						<button
							onClick={() => handleApiCall("subscribe", selectedFundId)}
							disabled={!selectedFundId}
						>
							Suscribir
						</button>
					</div>
					{message && <p className='message'>{message}</p>}
					{error && <p className='error'>{error}</p>}
				</div>

				<div className='history-card'>
					<h2>Historial de Transacciones</h2>
					<div className='table-container'>
						<table>
							<thead>
								<tr>
									<th>Tipo</th>
									<th>Fondo</th>
									<th>Monto</th>
									<th>Fecha</th>
								</tr>
							</thead>
							<tbody>
								{history.map((tx) => (
									<tr key={tx.record_id}>
										<td>{tx.transaction_type}</td>
										<td>{tx.fund_name}</td>
										<td>${new Intl.NumberFormat("es-CO").format(tx.amount)}</td>
										<td>
											{new Date(tx.record_id.split("#")[1]).toLocaleString()}
										</td>
									</tr>
								))}
							</tbody>
						</table>
					</div>
				</div>
			</header>
		</div>
	);
}

export default App;
