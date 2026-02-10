"""
Forex Factory News Scraper
Scrape economic calendar dan news dari ForexFactory.com
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
import json


class ForexFactoryNewsScraper:
    """Scraper untuk mendapatkan news dari Forex Factory"""
    
    def __init__(self):
        """Initialize Forex Factory scraper"""
        self.base_url = "https://www.forexfactory.com"
        self.calendar_url = f"{self.base_url}/calendar"
        
        # Headers untuk bypass blocking
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        # Impact levels
        self.impact_levels = {
            'high': 3,      # Red flag - high impact
            'medium': 2,    # Orange flag - medium impact
            'low': 1,       # Yellow flag - low impact
            'holiday': 0    # Holiday/no impact
        }
        
        # Cache untuk avoid duplicate
        self.processed_events = set()
    
    def get_calendar_events(self, date: Optional[str] = None) -> List[Dict]:
        """
        Get economic calendar events from Forex Factory
        
        Args:
            date: Date in format 'YYYY-MM-DD' (default: today)
        
        Returns:
            List of calendar events
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Format date untuk URL
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        month = date_obj.strftime('%b').lower()
        day = date_obj.day
        year = date_obj.year
        
        # URL format: /calendar?month=feb.2024
        url = f"{self.calendar_url}?day={month}{day}.{year}"
        
        try:
            print(f"📡 Fetching Forex Factory calendar: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                print(f"❌ Failed to fetch: Status {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Parse calendar table
            events = self._parse_calendar_table(soup, date_obj)
            
            print(f"✅ Found {len(events)} events from Forex Factory")
            return events
        
        except Exception as e:
            print(f"❌ Error scraping Forex Factory: {e}")
            return []
    
    def _parse_calendar_table(self, soup: BeautifulSoup, date: datetime) -> List[Dict]:
        """Parse calendar table from HTML"""
        events = []
        
        # Find calendar table
        calendar_rows = soup.find_all('tr', class_='calendar__row')
        
        if not calendar_rows:
            print("⚠️ No calendar rows found")
            return []
        
        current_time = None
        
        for row in calendar_rows:
            try:
                # Get time
                time_cell = row.find('td', class_='calendar__time')
                if time_cell and time_cell.text.strip():
                    current_time = time_cell.text.strip()
                
                # Get currency
                currency_cell = row.find('td', class_='calendar__currency')
                if not currency_cell:
                    continue
                currency = currency_cell.text.strip()
                
                # Get impact
                impact_cell = row.find('td', class_='calendar__impact')
                impact = 'low'
                if impact_cell:
                    impact_span = impact_cell.find('span')
                    if impact_span:
                        impact_class = impact_span.get('class', [])
                        if 'icon--ff-impact-red' in impact_class:
                            impact = 'high'
                        elif 'icon--ff-impact-ora' in impact_class:
                            impact = 'medium'
                        elif 'icon--ff-impact-yel' in impact_class:
                            impact = 'low'
                
                # Get event name
                event_cell = row.find('td', class_='calendar__event')
                if not event_cell:
                    continue
                event_name = event_cell.text.strip()
                
                # Get actual, forecast, previous values
                actual_cell = row.find('td', class_='calendar__actual')
                forecast_cell = row.find('td', class_='calendar__forecast')
                previous_cell = row.find('td', class_='calendar__previous')
                
                actual = actual_cell.text.strip() if actual_cell else None
                forecast = forecast_cell.text.strip() if forecast_cell else None
                previous = previous_cell.text.strip() if previous_cell else None
                
                # Create event ID untuk avoid duplicates
                event_id = f"{date.strftime('%Y%m%d')}_{current_time}_{currency}_{event_name}"
                
                if event_id in self.processed_events:
                    continue
                
                # Create event dict
                event = {
                    'id': event_id,
                    'date': date.strftime('%Y-%m-%d'),
                    'time': current_time,
                    'currency': currency,
                    'impact': impact,
                    'impact_score': self.impact_levels.get(impact, 0),
                    'event': event_name,
                    'actual': actual,
                    'forecast': forecast,
                    'previous': previous,
                    'source': 'ForexFactory'
                }
                
                events.append(event)
                self.processed_events.add(event_id)
            
            except Exception as e:
                continue
        
        return events
    
    def get_high_impact_events(self, hours_ahead: int = 2) -> List[Dict]:
        """
        Get upcoming high impact events dalam X jam ke depan
        
        Args:
            hours_ahead: Berapa jam ke depan yang akan dicek
        
        Returns:
            List of high impact events
        """
        # Get today's events
        today_events = self.get_calendar_events()
        
        # Filter high impact only
        high_impact = [e for e in today_events if e['impact'] == 'high']
        
        # Filter upcoming events (dalam X jam ke depan)
        now = datetime.now()
        upcoming = []
        
        for event in high_impact:
            try:
                # Parse event time
                event_time_str = event['time']
                if event_time_str and event_time_str != 'All Day':
                    # Format bisa: "8:30am" atau "1:00pm"
                    event_datetime = datetime.strptime(
                        f"{event['date']} {event_time_str}", 
                        '%Y-%m-%d %I:%M%p'
                    )
                    
                    # Check if within hours_ahead
                    time_diff = (event_datetime - now).total_seconds() / 3600
                    if -1 <= time_diff <= hours_ahead:  # -1 untuk event yang baru lewat
                        upcoming.append(event)
            except:
                continue
        
        return upcoming
    
    def create_news_summary(self, event: Dict) -> str:
        """
        Create news summary dari event untuk sentiment analysis
        
        Args:
            event: Event dictionary
        
        Returns:
            News summary text
        """
        currency = event['currency']
        event_name = event['event']
        impact = event['impact']
        actual = event.get('actual')
        forecast = event.get('forecast')
        previous = event.get('previous')
        
        # Build summary
        summary = f"{currency} - {event_name} ({impact.upper()} IMPACT)"
        
        # Add comparison if available
        if actual and forecast:
            try:
                # Remove non-numeric characters
                actual_val = float(actual.replace('%', '').replace('K', '000').replace('M', '000000').replace('B', '000000000'))
                forecast_val = float(forecast.replace('%', '').replace('K', '000').replace('M', '000000').replace('B', '000000000'))
                
                if actual_val > forecast_val:
                    summary += f" - Better than expected! Actual {actual} vs Forecast {forecast}"
                elif actual_val < forecast_val:
                    summary += f" - Worse than expected! Actual {actual} vs Forecast {forecast}"
                else:
                    summary += f" - As expected: {actual}"
            except:
                if actual:
                    summary += f" - Result: {actual}"
        elif actual:
            summary += f" - Result: {actual}"
        
        if previous:
            summary += f" (Previous: {previous})"
        
        return summary
    
    def get_currency_specific_news(self, currency: str) -> List[Dict]:
        """
        Get news untuk currency tertentu
        
        Args:
            currency: Currency code (USD, EUR, GBP, etc.)
        
        Returns:
            List of events untuk currency tersebut
        """
        all_events = self.get_calendar_events()
        return [e for e in all_events if e['currency'] == currency]


class ForexFactoryNewsAnalyzer:
    """Analyzer untuk convert Forex Factory events ke trading signals"""
    
    def __init__(self):
        """Initialize analyzer"""
        # Event types dan expected impact
        self.bullish_events = {
            # Employment
            'nfp': 0.8,
            'non-farm': 0.8,
            'employment': 0.6,
            'unemployment': -0.6,  # Lower unemployment = bullish
            'jobless': -0.6,
            
            # GDP & Growth
            'gdp': 0.7,
            'retail sales': 0.6,
            'manufacturing': 0.5,
            'pmi': 0.5,
            
            # Inflation (moderate inflation = bullish for currency)
            'cpi': 0.5,
            'inflation': 0.5,
            
            # Central Bank
            'interest rate': 0.9,
            'rate decision': 0.9,
            'fomc': 0.8,
            'ecb': 0.8,
            'boe': 0.8,
        }
    
    def analyze_event(self, event: Dict) -> Dict:
        """
        Analyze event dan generate trading signal
        
        Args:
            event: Event dari ForexFactory
        
        Returns:
            Analysis result dengan sentiment
        """
        currency = event['currency']
        event_name = event['event'].lower()
        actual = event.get('actual')
        forecast = event.get('forecast')
        previous = event.get('previous')
        impact = event['impact']
        
        # Default sentiment
        sentiment = 'NEUTRAL'
        sentiment_score = 0.0
        strength = 'weak'
        
        # Check if we can compare actual vs forecast
        if actual and forecast:
            try:
                # Clean values
                actual_clean = actual.replace('%', '').replace('K', '').replace('M', '').replace('B', '')
                forecast_clean = forecast.replace('%', '').replace('K', '').replace('M', '').replace('B', '')
                
                actual_val = float(actual_clean)
                forecast_val = float(forecast_clean)
                
                # Calculate difference percentage
                diff_pct = ((actual_val - forecast_val) / abs(forecast_val)) * 100 if forecast_val != 0 else 0
                
                # Determine if event is bullish or bearish type
                event_multiplier = 0.5  # Default
                for keyword, multiplier in self.bullish_events.items():
                    if keyword in event_name:
                        event_multiplier = multiplier
                        break
                
                # Calculate sentiment
                # Positive difference = good news (usually)
                if diff_pct > 0:
                    sentiment_score = min(diff_pct / 100 * event_multiplier, 1.0)
                    sentiment = 'LONG' if sentiment_score > 0.3 else 'NEUTRAL'
                elif diff_pct < 0:
                    sentiment_score = max(diff_pct / 100 * event_multiplier, -1.0)
                    sentiment = 'SHORT' if sentiment_score < -0.3 else 'NEUTRAL'
                
                # Adjust by impact level
                if impact == 'high':
                    sentiment_score *= 1.5
                elif impact == 'medium':
                    sentiment_score *= 1.0
                else:
                    sentiment_score *= 0.5
                
                # Normalize
                sentiment_score = max(min(sentiment_score, 1.0), -1.0)
                
                # Determine strength
                abs_score = abs(sentiment_score)
                if abs_score >= 0.7:
                    strength = 'very_strong'
                elif abs_score >= 0.5:
                    strength = 'strong'
                elif abs_score >= 0.3:
                    strength = 'moderate'
                else:
                    strength = 'weak'
            
            except:
                pass
        
        return {
            'event': event,
            'sentiment_score': round(sentiment_score, 3),
            'signal': sentiment,
            'strength': strength,
            'affected_currencies': [currency],
            'news_text': self.create_news_text(event, sentiment_score),
            'source': 'ForexFactory'
        }
    
    def create_news_text(self, event: Dict, sentiment_score: float) -> str:
        """Create descriptive news text"""
        currency = event['currency']
        event_name = event['event']
        actual = event.get('actual', 'N/A')
        forecast = event.get('forecast', 'N/A')
        
        direction = "positive" if sentiment_score > 0 else "negative" if sentiment_score < 0 else "neutral"
        
        text = f"{currency} {event_name}: {direction.upper()} result. "
        if actual != 'N/A':
            text += f"Actual: {actual}"
            if forecast != 'N/A':
                text += f" vs Forecast: {forecast}"
        
        return text


# Demo & Testing
if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║          FOREX FACTORY NEWS SCRAPER - DEMO                       ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize scraper
    scraper = ForexFactoryNewsScraper()
    analyzer = ForexFactoryNewsAnalyzer()
    
    print("\n1️⃣  Fetching today's calendar events...\n")
    
    # Get today's events
    events = scraper.get_calendar_events()
    
    if events:
        print(f"Found {len(events)} events today:\n")
        
        # Group by impact
        high_impact = [e for e in events if e['impact'] == 'high']
        medium_impact = [e for e in events if e['impact'] == 'medium']
        
        print(f"🔴 HIGH IMPACT: {len(high_impact)} events")
        for event in high_impact[:5]:  # Show first 5
            print(f"   • {event['time']} - {event['currency']} - {event['event']}")
            if event.get('actual'):
                print(f"     Actual: {event['actual']} | Forecast: {event.get('forecast', 'N/A')}")
        
        print(f"\n🟠 MEDIUM IMPACT: {len(medium_impact)} events")
        for event in medium_impact[:3]:  # Show first 3
            print(f"   • {event['time']} - {event['currency']} - {event['event']}")
    
    print("\n\n2️⃣  Getting upcoming high impact events...\n")
    
    upcoming = scraper.get_high_impact_events(hours_ahead=24)
    
    if upcoming:
        print(f"Found {len(upcoming)} upcoming high impact events in next 24h:\n")
        for event in upcoming:
            print(f"📅 {event['time']} - {event['currency']} - {event['event']}")
    else:
        print("No upcoming high impact events in next 24h")
    
    print("\n\n3️⃣  Analyzing events for trading signals...\n")
    
    # Analyze events yang punya actual values
    events_with_data = [e for e in events if e.get('actual')]
    
    if events_with_data:
        for event in events_with_data[:5]:  # Analyze first 5
            analysis = analyzer.analyze_event(event)
            
            print(f"📊 {event['currency']} - {event['event']}")
            print(f"   Signal: {analysis['signal']}")
            print(f"   Sentiment Score: {analysis['sentiment_score']:.3f}")
            print(f"   Strength: {analysis['strength']}")
            print(f"   News: {analysis['news_text']}\n")
    else:
        print("No events with actual data yet (events haven't occurred)")
    
    print("\n✅ Demo complete!")
