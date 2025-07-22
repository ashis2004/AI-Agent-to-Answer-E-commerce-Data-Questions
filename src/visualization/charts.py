from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot

import config


class ChartGenerator:
    """Generates charts and visualizations for query results"""
    
    def __init__(self):
        self.charts_dir = config.PROJECT_ROOT / "static" / "charts"
        self.charts_dir.mkdir(parents=True, exist_ok=True)
    
    def create_chart(self, data: List[Dict[str, Any]], question: str) -> Optional[str]:
        """Create appropriate chart based on data and question"""
        if not data:
            return None
        
        df = pd.DataFrame(data)
        question_lower = question.lower()
        
        # Determine chart type based on question and data
        if "sales" in question_lower and "product" in question_lower:
            return self._create_sales_chart(df, question)
        elif "roas" in question_lower:
            return self._create_roas_chart(df, question)
        elif "cpc" in question_lower or "cost per click" in question_lower:
            return self._create_cpc_chart(df, question)
        elif "performance" in question_lower:
            return self._create_performance_chart(df, question)
        else:
            return self._create_generic_chart(df, question)
    
    def _create_sales_chart(self, df: pd.DataFrame, question: str) -> str:
        """Create sales-related charts"""
        if 'product_name' in df.columns and 'total_sales' in df.columns:
            fig = px.bar(
                df, 
                x='product_name', 
                y='total_sales',
                title='Product Sales Performance',
                labels={'total_sales': 'Total Sales ($)', 'product_name': 'Product'},
                color='total_sales',
                color_continuous_scale='Blues'
            )
            fig.update_layout(xaxis_tickangle=-45)
        elif 'total_sales' in df.columns:
            # Single value - create gauge chart
            total_sales = df['total_sales'].iloc[0]
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=total_sales,
                title={'text': "Total Sales ($)"},
                gauge={
                    'axis': {'range': [None, total_sales * 1.2]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, total_sales * 0.5], 'color': "lightgray"},
                        {'range': [total_sales * 0.5, total_sales], 'color': "gray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': total_sales * 0.9
                    }
                }
            ))
        else:
            return self._create_generic_chart(df, question)
        
        return self._save_chart(fig, "sales_chart")
    
    def _create_roas_chart(self, df: pd.DataFrame, question: str) -> str:
        """Create RoAS visualization"""
        if 'roas' in df.columns:
            roas_value = df['roas'].iloc[0]
            
            # Create gauge chart for RoAS
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=roas_value,
                title={'text': "Return on Ad Spend (RoAS)"},
                delta={'reference': 2.0},  # Typical good RoAS benchmark
                gauge={
                    'axis': {'range': [None, max(5, roas_value * 1.2)]},
                    'bar': {'color': "darkgreen"},
                    'steps': [
                        {'range': [0, 1], 'color': "red"},
                        {'range': [1, 2], 'color': "yellow"},
                        {'range': [2, 5], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 2.0
                    }
                }
            ))
            
            # Add annotation
            fig.add_annotation(
                text=f"RoAS: {roas_value:.2f}<br>{'Excellent' if roas_value > 3 else 'Good' if roas_value > 2 else 'Needs Improvement'}",
                xref="paper", yref="paper",
                x=0.5, y=0.1, showarrow=False,
                font=dict(size=14)
            )
        else:
            return self._create_generic_chart(df, question)
        
        return self._save_chart(fig, "roas_chart")
    
    def _create_cpc_chart(self, df: pd.DataFrame, question: str) -> str:
        """Create CPC-related charts"""
        if 'product_name' in df.columns and 'cpc' in df.columns:
            fig = px.bar(
                df, 
                x='product_name', 
                y='cpc',
                title='Cost Per Click by Product',
                labels={'cpc': 'Cost Per Click ($)', 'product_name': 'Product'},
                color='cpc',
                color_continuous_scale='Reds'
            )
            fig.update_layout(xaxis_tickangle=-45)
        else:
            return self._create_generic_chart(df, question)
        
        return self._save_chart(fig, "cpc_chart")
    
    def _create_performance_chart(self, df: pd.DataFrame, question: str) -> str:
        """Create performance overview charts"""
        # Create multi-metric chart
        if len(df.columns) > 2:
            # Select numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if len(numeric_cols) >= 2:
                fig = px.scatter_matrix(
                    df, 
                    dimensions=numeric_cols[:4],  # Limit to first 4 numeric columns
                    title='Performance Metrics Overview'
                )
            else:
                return self._create_generic_chart(df, question)
        else:
            return self._create_generic_chart(df, question)
        
        return self._save_chart(fig, "performance_chart")
    
    def _create_generic_chart(self, df: pd.DataFrame, question: str) -> str:
        """Create generic chart based on data structure"""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
            # Bar chart
            fig = px.bar(
                df, 
                x=categorical_cols[0], 
                y=numeric_cols[0],
                title=f'Analysis: {question[:50]}...' if len(question) > 50 else f'Analysis: {question}',
                color=numeric_cols[0] if len(df) > 1 else None
            )
            fig.update_layout(xaxis_tickangle=-45)
        elif len(numeric_cols) >= 2:
            # Scatter plot
            fig = px.scatter(
                df, 
                x=numeric_cols[0], 
                y=numeric_cols[1],
                title=f'Analysis: {question[:50]}...' if len(question) > 50 else f'Analysis: {question}',
                size=numeric_cols[2] if len(numeric_cols) > 2 else None
            )
        elif len(numeric_cols) == 1:
            # Single metric - gauge or bar
            if len(df) == 1:
                # Single value - gauge
                value = df[numeric_cols[0]].iloc[0]
                fig = go.Figure(go.Indicator(
                    mode="number",
                    value=value,
                    title={'text': numeric_cols[0].replace('_', ' ').title()},
                ))
            else:
                # Multiple values - bar chart
                fig = px.bar(
                    df, 
                    y=numeric_cols[0],
                    title=f'Analysis: {question[:50]}...' if len(question) > 50 else f'Analysis: {question}'
                )
        else:
            # Table view for non-numeric data
            fig = go.Figure(data=[go.Table(
                header=dict(values=list(df.columns),
                           fill_color='paleturquoise',
                           align='left'),
                cells=dict(values=[df[col] for col in df.columns],
                          fill_color='lavender',
                          align='left'))
            ])
            fig.update_layout(title=f'Data Table: {question[:50]}...' if len(question) > 50 else f'Data Table: {question}')
        
        return self._save_chart(fig, "generic_chart")
    
    def _save_chart(self, fig: go.Figure, chart_name: str) -> str:
        """Save chart and return file path"""
        # Update layout for better appearance
        fig.update_layout(
            template="plotly_white",
            font=dict(family="Arial, sans-serif", size=12),
            title_font_size=16,
            showlegend=True
        )
        
        # Generate filename
        filename = f"{chart_name}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = self.charts_dir / filename
        
        # Save chart
        plot(fig, filename=str(filepath), auto_open=False)
        
        # Return relative path for web access
        return f"/charts/{filename}"
    
    def create_dashboard(self, all_data: Dict[str, List[Dict[str, Any]]]) -> str:
        """Create a comprehensive dashboard with multiple charts"""
        from plotly.subplots import make_subplots

        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Sales Overview', 'Ad Performance', 'Product Metrics', 'Summary'),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "bar"}, {"type": "indicator"}]]
        )
        
        # Add charts to subplots (implementation depends on available data)
        # This is a placeholder for a more complex dashboard
        
        fig.update_layout(
            height=800,
            title_text="E-commerce Performance Dashboard",
            template="plotly_white"
        )
        
        return self._save_chart(fig, "dashboard")
