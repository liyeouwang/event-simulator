#include <stdio.h>
#include <stdlib.h>
#include <fstream> //ifstream
#include <string>       // std::string
#include <iostream>     // std::cout
#include <sstream>      // std::istringstream
using namespace std;

#include <vector>
#include <time.h>       /* time */
#include <map>

#define REQUEST_ARRIVAL 0
#define DECISION 1
#define PROPAGATION 2
#define EXECUTION 3
#define DELIVERY 4

class Event
{
	public:
		int type;
		int ID;
		int nextTime;

	Event createEvent()
	{
		Event newEvent;
		switch(this->type)
		{
			case(REQUEST_ARRIVAL):
				//DECISION
				newEvent.type = DECISION;
				break;
			case(DECISION):
			{
				//PROPAGATION or EXECUTION or DELIVERY
				int nextPossibleEvents[3]={EXECUTION, PROPAGATION, DELIVERY};
				int randIndex = rand() % 3;
				newEvent.type = nextPossibleEvents[randIndex];				
				break;
			}
				
			case(PROPAGATION):
			{
				break;
			}
				
			case(EXECUTION):
				//delivery or propagation
				newEvent.type = newEvent.type = (rand() > RAND_MAX/2) ? DELIVERY : PROPAGATION;
				break;
			case(DELIVERY):
				//non
				newEvent.type = DELIVERY;
				break;
			default:
				break;
		}

		return newEvent;
	}
};

void removeEvent(vector<Event> &vec_event, int &num_events)
{
	//remove event	
	vec_event.erase(vec_event.begin());
	num_events--;
}

void showAllEvents(int num_events, vector<Event> vec_event)
{
	for(int i =0; i<num_events; i++)
	{
		switch(vec_event[i].type)
		{
			case(REQUEST_ARRIVAL):
				cout<<"event "<<vec_event[i].ID<<": (request arrival) "<<endl;
				break;
			case(DECISION):
				cout<<"event "<<vec_event[i].ID<<": (decision) "<<endl;
				break;
			case(PROPAGATION):
				cout<<"event "<<vec_event[i].ID<<": (propagation) "<<endl;
				break;
			case(EXECUTION):
				cout<<"event "<<vec_event[i].ID<<": (execution) "<<endl;
				break;
			case(DELIVERY):
				cout<<"event "<<vec_event[i].ID<<": (delivery) "<<endl;
				break;
		}
		

	}
	cout<<endl;
}

void scheduleNewEvent(vector<Event> &vec_event, Event currentEvent, Event newEvent)
{
	//randomly insert into event queue 
	int time = rand() % (vec_event.size())+1; 
	vec_event.insert(vec_event.begin()+time, newEvent);
	/*
	if (time>=0)
			vec_event.insert(vec_event.begin()+time, newEvent);
		else 
			vec_event.push_back(newEvent);
	*/
	//return time;
} 

//process the event 
void runEvent(vector<Event> &vec_event, int &eventId, int &num_events)
{
	Event currentEvent = vec_event.front();

	//DELIVERY and PROPAGATION will not create new event
	if(currentEvent.type != DELIVERY && currentEvent.type != PROPAGATION)
	{
		//create a new event 
		Event newEvent = currentEvent.createEvent();
		newEvent.ID = ++eventId;
		num_events++;
		scheduleNewEvent(vec_event, currentEvent, newEvent);
	}
	//remove current event
	removeEvent(vec_event, num_events);
}

//read all events from input file
void readEvents(vector<Event> &vec_event, map<string, int> eventMap,
	int &eventId, int &num_events, vector<Event> eventQueue[])
{
	map<string, int>::iterator iter;
	ifstream input("events.dat"); 
	string s;
	input>>s; //num_servers
	//int num_servers = atoi(s.c_str());
	input>>s; 
	num_events = atoi(s.c_str());

	
	eventId = 0;
	for(int i =0; i<num_events; i++)
	{
		Event e;
		input>>s;
		iter = eventMap.find(s);
		e.type = iter->second;
		//input>>e.nextTime;
		e.ID=++eventId;
		vec_event.push_back(e); 

		input>>s;
		int server = atoi(s.c_str());
		eventQueue[server].push_back(e);

	}
	
	//store each event in its corresponding server event queue  
	for(int s = 0; s<4; s++)
	{
		for(int i=0; i<eventQueue[s].size(); i++)
		{
			cout<<"server "<<s<<": "<<eventQueue[s][i].type<<endl;
		}
		
	}
	
}
//mapping from input string to int type 
void setMap(map<string, int> &eventMap)
{
	eventMap["decision"] = DECISION;
	eventMap["request_arrival"] = REQUEST_ARRIVAL;
	eventMap["propagation"] = PROPAGATION;
	eventMap["execution"] = EXECUTION;
	eventMap["delivery"] = DELIVERY;
}

int main(int argc, char* argv[])
{
	/* initialize random seed: */
	srand (time(NULL));

	//mapping from string to corresponding type 
	map<string, int> eventMap;	
	setMap(eventMap);

	//event queue （all events）
	vector<Event> vec_event;

	//read the number of servers 
	ifstream input("events.dat"); 
	string s;
	input>>s;
	int num_servers = atoi(s.c_str());

	//events of each server
	vector<Event> eventQueue[num_servers];

	int num_events;
	int eventId;

	readEvents(vec_event, eventMap, eventId, num_events, eventQueue);
	cout<<"t= 0"<<endl;
	showAllEvents(num_events, vec_event);

	int simulationTime = num_events*2;
	for(int t=1; t<simulationTime; t++)
	{
		cout<<"t= "<<t<<endl;
		if(! vec_event.empty ())
		{
			runEvent(vec_event, eventId, num_events);
		}
		showAllEvents(num_events, vec_event);
	}
	// hi~
	return 0;
}

	//for each time steps 
		//if(! eventQueue.empty ())
			//process an event
				//create new events
				//rearange the event queue (push back)
			//delete the event
