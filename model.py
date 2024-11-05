"""
Implements a runtime data model that can be used to access
the properties contained in the issues JSON.
"""

from typing import List, Dict, Set, Tuple
from enum import Enum
from datetime import datetime
from dateutil import parser


class State(str, Enum):
    """
    Whether issue is open or closed.
    """
    open = 'open'
    closed = 'closed'


class Event:
    
    def __init__(self, jobj:any):
        self.event_type:str = None
        self.author:str = None
        self.event_date:datetime = None
        self.label:str = None
        self.comment:str = None
        
        if jobj is not None:
            self.from_json(jobj)
    
    def from_json(self, jobj:any):
        self.event_type = jobj.get('event_type')
        self.author = jobj.get('author')
        try:
            self.event_date = parser.parse(jobj.get('event_date'))
        except:
            pass
        self.label = jobj.get('label')
        self.comment = jobj.get('comment')
        
        
class Issue:
    
    def __init__(self, jobj:any=None):
        self.url:str = None
        self.creator:str = None
        self.labels:List[str] = []
        self.state:State = None
        self.assignees:List[str] = []
        self.title:str = None
        self.text:str = None
        self.number: int = id if id is not None else -1  # Assign id to number
        self.created_date:datetime = None
        self.updated_date:datetime = None
        self.timeline_url:str = None
        self.events:List[Event] = []
        
        if jobj is not None:
            self.from_json(jobj)
    
    def from_json(self, jobj: any):
        self.url = jobj.get('url')
        self.creator = jobj.get('creator')
        self.labels = jobj.get('labels', [])
        
        # Handle state assignment
        state_value = jobj.get('state')
        if state_value in State.__members__:
            self.state = State[state_value]
        else:
            self.state = None  # or a default state, if applicable
        
        self.assignees = jobj.get('assignees', [])
        self.title = jobj.get('title')
        self.text = jobj.get('text')

        # Safely convert number to int
        try:
            self.number = int(jobj.get('number', '-1'))
        except ValueError:
            self.number = -1  # Set to -1 if conversion fails
        
        # Parse dates safely
        self.created_date = self._parse_date(jobj.get('created_date'))
        self.updated_date = self._parse_date(jobj.get('updated_date'))
        
        self.timeline_url = jobj.get('timeline_url')
        self.events = [Event(jevent) for jevent in jobj.get('events', [])]

    def _parse_date(self, date_str):
        """Helper method to parse dates, returning None if parsing fails."""
        if date_str:
            try:
                return parser.parse(date_str)
            except (ValueError, TypeError):
                return None
        return None