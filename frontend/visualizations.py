"""
Visualizations - Creates music-inspired charts and graphs
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple
import config
import io
import base64


class MusicVisualizer:
    """Creates music-inspired visualizations for lyrics analysis"""

    def __init__(self):
        """Initialize the visualizer with color palette"""
        self.colors = config.COLOR_PALETTE

    def create_word_cloud(
        self,
        word_frequency: Dict[str, int],
        width: int = 800,
        height: int = 400
    ) -> str:
        """
        Create a word cloud visualization

        Args:
            word_frequency: Dictionary of word frequencies
            width: Width of the image
            height: Height of the image

        Returns:
            Base64 encoded image string
        """
        # Create word cloud
        wc = WordCloud(
            width=width,
            height=height,
            background_color=self.colors['background'],
            colormap='plasma',  # Purple/pink gradient
            max_words=100,
            relative_scaling=0.5,
            min_font_size=10,
        ).generate_from_frequencies(word_frequency)

        # Convert to image
        fig, ax = plt.subplots(figsize=(width/100, height/100))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        plt.tight_layout(pad=0)

        # Convert to base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', facecolor=self.colors['background'])
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode()
        plt.close()

        return img_str

    def create_top_words_chart(
        self,
        top_words: List[Tuple[str, int]],
        top_n: int = 20
    ) -> go.Figure:
        """
        Create interactive bar chart of top words

        Args:
            top_words: List of (word, count) tuples
            top_n: Number of top words to display

        Returns:
            Plotly figure
        """
        # Prepare data
        words = [w[0] for w in top_words[:top_n]]
        counts = [w[1] for w in top_words[:top_n]]

        # Reverse for better display (highest at top)
        words = words[::-1]
        counts = counts[::-1]

        # Create gradient colors
        colors_gradient = self._create_gradient(len(words))

        # Create figure
        fig = go.Figure()

        fig.add_trace(go.Bar(
            y=words,
            x=counts,
            orientation='h',
            marker=dict(
                color=colors_gradient,
                line=dict(color=self.colors['accent'], width=1)
            ),
            text=counts,
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Used %{x} times<extra></extra>'
        ))

        # Update layout
        fig.update_layout(
            title={
                'text': f'Top {top_n} Most Used Words',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': self.colors['text_primary']}
            },
            xaxis_title='Frequency',
            yaxis_title='',
            plot_bgcolor=self.colors['background'],
            paper_bgcolor=self.colors['background'],
            font=dict(color=self.colors['text_secondary'], size=12),
            height=600,
            margin=dict(l=150, r=50, t=80, b=50),
            xaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.1)',
                showgrid=True
            ),
            yaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.1)',
            )
        )

        return fig

    def create_diversity_gauge(self, diversity_score: float) -> go.Figure:
        """
        Create a gauge chart for vocabulary diversity

        Args:
            diversity_score: Diversity score (0-10)

        Returns:
            Plotly figure
        """
        # Determine color based on score
        if diversity_score >= 7:
            gauge_color = '#06ffa5'  # Excellent - green
        elif diversity_score >= 5:
            gauge_color = '#8338ec'  # Good - purple
        else:
            gauge_color = '#ff006e'  # Needs improvement - pink

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=diversity_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={
                'text': "Vocabulary Diversity Score",
                'font': {'size': 24, 'color': self.colors['text_primary']}
            },
            gauge={
                'axis': {'range': [None, 10], 'tickwidth': 1, 'tickcolor': self.colors['text_secondary']},
                'bar': {'color': gauge_color},
                'bgcolor': "rgba(255, 255, 255, 0.1)",
                'borderwidth': 2,
                'bordercolor': self.colors['text_secondary'],
                'steps': [
                    {'range': [0, 3], 'color': 'rgba(255, 0, 110, 0.3)'},
                    {'range': [3, 7], 'color': 'rgba(131, 56, 236, 0.3)'},
                    {'range': [7, 10], 'color': 'rgba(6, 255, 165, 0.3)'}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': diversity_score
                }
            }
        ))

        fig.update_layout(
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['background'],
            font={'color': self.colors['text_primary']},
            height=300
        )

        return fig

    def create_comparison_chart(self, comparison_df) -> go.Figure:
        """
        Create comparison chart for multiple artists

        Args:
            comparison_df: DataFrame with artist comparison data

        Returns:
            Plotly figure
        """
        fig = go.Figure()

        # Unique words comparison
        fig.add_trace(go.Bar(
            name='Unique Words',
            x=comparison_df['Artist'],
            y=comparison_df['Unique Words'],
            marker_color=self.colors['primary'],
            text=comparison_df['Unique Words'],
            textposition='outside'
        ))

        # Diversity score (scaled for visibility)
        fig.add_trace(go.Scatter(
            name='Diversity Score (×100)',
            x=comparison_df['Artist'],
            y=comparison_df['Diversity Score'] * 100,
            mode='lines+markers',
            marker=dict(size=12, color=self.colors['accent']),
            line=dict(color=self.colors['accent'], width=3),
            yaxis='y2'
        ))

        # Update layout
        fig.update_layout(
            title={
                'text': 'Artist Vocabulary Comparison',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': self.colors['text_primary']}
            },
            xaxis_title='Artist',
            yaxis_title='Unique Words',
            yaxis2=dict(
                title='Diversity Score (×100)',
                overlaying='y',
                side='right',
                showgrid=False
            ),
            plot_bgcolor=self.colors['background'],
            paper_bgcolor=self.colors['background'],
            font=dict(color=self.colors['text_secondary']),
            height=500,
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        return fig

    def create_timeline_chart(self, timeline_df) -> go.Figure:
        """
        Create timeline chart showing vocabulary evolution

        Args:
            timeline_df: DataFrame with year and vocabulary data

        Returns:
            Plotly figure
        """
        if timeline_df.empty:
            # Return empty figure with message
            fig = go.Figure()
            fig.add_annotation(
                text="No timeline data available (year information missing)",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color=self.colors['text_secondary'])
            )
            fig.update_layout(
                paper_bgcolor=self.colors['background'],
                plot_bgcolor=self.colors['background'],
                height=300
            )
            return fig

        fig = go.Figure()

        # Area chart for average unique words
        fig.add_trace(go.Scatter(
            x=timeline_df['year'],
            y=timeline_df['avg_unique_words'],
            mode='lines+markers',
            name='Avg Unique Words',
            fill='tozeroy',
            line=dict(color=self.colors['secondary'], width=3),
            marker=dict(size=8, color=self.colors['accent']),
            hovertemplate='<b>Year %{x}</b><br>Avg Unique Words: %{y:.1f}<extra></extra>'
        ))

        # Update layout
        fig.update_layout(
            title={
                'text': 'Vocabulary Evolution Over Time',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': self.colors['text_primary']}
            },
            xaxis_title='Year',
            yaxis_title='Average Unique Words per Song',
            plot_bgcolor=self.colors['background'],
            paper_bgcolor=self.colors['background'],
            font=dict(color=self.colors['text_secondary']),
            height=400,
            xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
        )

        return fig

    def create_stats_cards_html(self, analysis: Dict) -> str:
        """
        Create HTML for statistics cards

        Args:
            analysis: Analysis dictionary

        Returns:
            HTML string
        """
        cards_html = f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0;">
            <div style="background: linear-gradient(135deg, {self.colors['primary']}, {self.colors['secondary']});
                        padding: 20px; border-radius: 10px; text-align: center;">
                <h3 style="margin: 0; color: white; font-size: 2em;">{analysis['unique_words']:,}</h3>
                <p style="margin: 5px 0 0 0; color: rgba(255,255,255,0.9);">Unique Words</p>
            </div>
            <div style="background: linear-gradient(135deg, {self.colors['secondary']}, {self.colors['accent']});
                        padding: 20px; border-radius: 10px; text-align: center;">
                <h3 style="margin: 0; color: white; font-size: 2em;">{analysis['total_songs_analyzed']}</h3>
                <p style="margin: 5px 0 0 0; color: rgba(255,255,255,0.9);">Songs Analyzed</p>
            </div>
            <div style="background: linear-gradient(135deg, {self.colors['accent']}, {self.colors['primary']});
                        padding: 20px; border-radius: 10px; text-align: center;">
                <h3 style="margin: 0; color: white; font-size: 2em;">{analysis['avg_unique_words_per_song']:.1f}</h3>
                <p style="margin: 5px 0 0 0; color: rgba(255,255,255,0.9);">Avg Words/Song</p>
            </div>
            <div style="background: linear-gradient(135deg, {self.colors['primary']}, {self.colors['accent']});
                        padding: 20px; border-radius: 10px; text-align: center;">
                <h3 style="margin: 0; color: white; font-size: 1.5em;">{analysis['top_words'][0][0] if analysis['top_words'] else 'N/A'}</h3>
                <p style="margin: 5px 0 0 0; color: rgba(255,255,255,0.9);">Most Used Word</p>
            </div>
        </div>
        """
        return cards_html

    def _create_gradient(self, n: int) -> List[str]:
        """
        Create a gradient of colors

        Args:
            n: Number of colors

        Returns:
            List of color strings
        """
        # Interpolate between gradient_start and gradient_end
        start_color = self.colors['gradient_start']
        end_color = self.colors['gradient_end']

        # Simple gradient (could be improved with proper color interpolation)
        colors = [self.colors['primary'] if i % 2 == 0 else self.colors['secondary']
                  for i in range(n)]

        return colors
