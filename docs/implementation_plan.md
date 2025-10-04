# WhatsApp Fitness Bot - Implementation Plan

## Overview
Build a WhatsApp-based AI fitness coaching bot for a 14-day experiment with 20 users. The bot discovers individual failure patterns and adapts workout plans to improve consistency.

## Architecture Principles
- **Minimal complexity**: Use simplest solution that works for 20 users
- **Stateless where possible**: Store state in database, not memory
- **Fail gracefully**: Always respond to users, even if analysis fails
- **Data-first**: Every interaction is valuable data for pattern discovery

## Implementation Phases

---

## Phase 1: Project Setup & Infrastructure (Day 1)

### Ticket 1.1: Initialize Python Project
**Priority:** Critical
**Estimated Time:** 2 hours

**Tasks:**
- Create project structure with Flask application
- Set up virtual environment with Python 3.11+
- Create requirements.txt with all dependencies
- Initialize git repository

**Acceptance Criteria:**
- [ ] Project runs locally with `flask run`
- [ ] All dependencies install without conflicts
- [ ] Health check endpoint `/health` returns 200 OK
- [ ] `.env.example` file with all required environment variables

**Files to Create:**
```
/
├── app.py
├── requirements.txt
├── runtime.txt (python-3.11.7)
├── .env.example
├── .gitignore
└── README.md
```

---

### Ticket 1.2: Configure Railway Deployment
**Priority:** Critical
**Estimated Time:** 1 hour

**Tasks:**
- Connect GitHub repository to Railway
- Configure environment variables in Railway
- Set up PostgreSQL database service
- Deploy initial application

**Acceptance Criteria:**
- [ ] Application deploys successfully to Railway
- [ ] PostgreSQL database is accessible
- [ ] Health endpoint accessible via public URL
- [ ] Auto-deploy enabled from main branch

---

### Ticket 1.3: Twilio WhatsApp Setup
**Priority:** Critical
**Estimated Time:** 2 hours

**Tasks:**
- Configure Twilio WhatsApp sandbox for development
- Set up webhook endpoint `/webhook/whatsapp`
- Implement basic echo bot for testing
- Configure message status callbacks

**Acceptance Criteria:**
- [ ] Can send "START" to WhatsApp number and receive response
- [ ] Webhook receives and processes incoming messages
- [ ] Delivery status tracked for outgoing messages
- [ ] Error handling for failed messages

**Code Structure:**
```python
# services/twilio_service.py
class TwilioService:
    def send_message(user_id: str, message: str) -> bool
    def validate_webhook(request) -> bool
    def parse_incoming_message(request) -> dict
```

---

## Phase 2: Database & Models (Day 1-2)

### Ticket 2.1: Database Schema & Models
**Priority:** Critical
**Estimated Time:** 3 hours

**Tasks:**
- Create SQLAlchemy models for all tables
- Set up Flask-Migrate for migrations
- Create initial migration scripts
- Add database connection pooling

**Acceptance Criteria:**
- [ ] All 5 tables created (users, daily_checkins, workout_plans, pattern_analyses, messages)
- [ ] Migrations run successfully
- [ ] Can perform CRUD operations on all models
- [ ] Unique constraints and indexes in place

**Models to Create:**
```python
# models/user.py
class User(db.Model):
    # All user fields from PRD

# models/daily_checkin.py
class DailyCheckin(db.Model):
    # Morning and evening check-in data

# models/workout_plan.py
class WorkoutPlan(db.Model):
    # Weekly schedules and adaptations

# models/pattern_analysis.py
class PatternAnalysis(db.Model):
    # Week 1 discoveries

# models/message.py
class Message(db.Model):
    # Conversation history
```

---

### Ticket 2.2: State Management System
**Priority:** High
**Estimated Time:** 2 hours

**Tasks:**
- Implement user state tracking (onboarding, week_1_active, etc.)
- Create state transition functions
- Add conversation context builder
- Implement session recovery logic

**Acceptance Criteria:**
- [ ] User state persists across messages
- [ ] Can retrieve user's current stage
- [ ] Conversation history accessible for context
- [ ] Handles mid-conversation interruptions

**Code Structure:**
```python
# services/state_manager.py
class StateManager:
    def get_user_state(user_id: str) -> str
    def transition_state(user_id: str, new_state: str)
    def get_conversation_context(user_id: str, limit: int = 10)
```

---

## Phase 3: Core Messaging Infrastructure (Day 2-3)

### Ticket 3.1: Message Router & Handler
**Priority:** Critical
**Estimated Time:** 3 hours

**Tasks:**
- Create central message router
- Implement handler registry pattern
- Add message type detection
- Create response queue system

**Acceptance Criteria:**
- [ ] Routes messages based on user state
- [ ] Handles concurrent users without conflicts
- [ ] Processes messages asynchronously
- [ ] Gracefully handles unknown message types

**Code Structure:**
```python
# services/message_handler.py
class MessageHandler:
    def route_message(user_id: str, message: str)
    def register_handler(state: str, handler: callable)
    def process_message(user_id: str, message: str, state: str)
```

---

### Ticket 3.2: Claude AI Integration
**Priority:** Critical
**Estimated Time:** 2 hours

**Tasks:**
- Integrate Anthropic Claude SDK
- Create prompt templates for different contexts
- Implement retry logic with exponential backoff
- Add response parsing and validation

**Acceptance Criteria:**
- [ ] Successfully calls Claude API
- [ ] Handles timeouts gracefully (30s limit)
- [ ] Parses structured responses (JSON)
- [ ] Falls back to default responses on failure

**Code Structure:**
```python
# services/claude_service.py
class ClaudeService:
    def generate_workout_plan(user_data: dict) -> dict
    def analyze_patterns(week_data: list) -> dict
    def generate_adaptive_plan(patterns: dict) -> dict
    def handle_general_question(context: str, question: str) -> str
```

---

### Ticket 3.3: APScheduler Setup
**Priority:** Critical
**Estimated Time:** 2 hours

**Tasks:**
- Configure BackgroundScheduler with UTC timezone
- Create job management system
- Implement morning/evening check-in schedulers
- Add job persistence across restarts

**Acceptance Criteria:**
- [ ] Scheduler starts with Flask app
- [ ] Jobs execute at correct times (London/Dublin timezone)
- [ ] Can add/remove jobs dynamically per user
- [ ] Jobs survive app restarts

**Code Structure:**
```python
# services/scheduler_service.py
class SchedulerService:
    def schedule_morning_checkin(user_id: str, time: str)
    def schedule_evening_checkin(user_id: str, time: str)
    def cancel_user_jobs(user_id: str)
    def reschedule_job(job_id: str, new_time: str)
```

---

## Phase 4: Onboarding Flow (Day 3-4)

### Ticket 4.1: Onboarding Conversation Flow
**Priority:** High
**Estimated Time:** 4 hours

**Tasks:**
- Implement 5-question onboarding sequence
- Create answer validation and parsing
- Build progressive state transitions
- Generate personalized Week 1 plan via Claude

**Acceptance Criteria:**
- [ ] User types "START" and receives welcome message
- [ ] All 5 questions asked in sequence
- [ ] Invalid answers trigger clarification requests
- [ ] Week 1 plan generated and sent after Q5
- [ ] First check-in scheduled for next morning

**Handlers to Create:**
```python
# handlers/onboarding.py
def handle_start(user_id: str)
def handle_q1_fitness_level(user_id: str, message: str)
def handle_q2_ideal_workout(user_id: str, message: str)
def handle_q3_week_structure(user_id: str, message: str)
def handle_q4_past_patterns(user_id: str, message: str)
def handle_q5_goals(user_id: str, message: str)
def generate_week1_plan(user_id: str)
```

---

### Ticket 4.2: Input Validation & Parsing
**Priority:** Medium
**Estimated Time:** 2 hours

**Tasks:**
- Create parsers for different input formats
- Implement flexible time parsing (6am, 6:00, 0600)
- Add number range validation (1-10 scales)
- Build error messages for invalid inputs

**Acceptance Criteria:**
- [ ] Parses sleep hours (decimal: 6.5)
- [ ] Validates 1-10 scale inputs
- [ ] Handles multiple date/time formats
- [ ] Provides clear correction messages

**Code Structure:**
```python
# utils/parsers.py
def parse_sleep_hours(input: str) -> float
def parse_scale_rating(input: str, min: int, max: int) -> int
def parse_time(input: str) -> str
def parse_checkin_response(message: str) -> dict
```

---

## Phase 5: Daily Check-in Flows (Day 4-5)

### Ticket 5.1: Morning Check-in System
**Priority:** High
**Estimated Time:** 3 hours

**Tasks:**
- Implement 6am automated message sender
- Parse morning check-in responses
- Handle partial responses
- Schedule follow-up if no response by 10am

**Acceptance Criteria:**
- [ ] Sends at exactly 6am user timezone
- [ ] Accepts format: "Sleep: X, Energy: Y, Stress: Z, Confidence: W"
- [ ] Saves all data to daily_checkins table
- [ ] Sends 10am reminder if no response
- [ ] Updates morning_checkin_complete flag

---

### Ticket 5.2: Evening Check-in System
**Priority:** High
**Estimated Time:** 3 hours

**Tasks:**
- Implement 8pm automated message sender
- Handle COMPLETED/SKIPPED/MODIFIED responses
- Collect skip reasons and insights
- Ask about tomorrow's concerns

**Acceptance Criteria:**
- [ ] Sends at exactly 8pm user timezone
- [ ] Processes completion status correctly
- [ ] For skips, collects reason and timing
- [ ] Increments day counter after check-in
- [ ] Triggers Day 7 analysis if applicable

---

### Ticket 5.3: Skip Handling & Data Collection
**Priority:** Medium
**Estimated Time:** 2 hours

**Tasks:**
- Create skip reason conversation flow
- Implement "what might have helped" questioning
- Tag skip patterns for analysis
- Maintain non-judgmental tone

**Acceptance Criteria:**
- [ ] Follows up skips with data questions
- [ ] Captures decision timing (morning/midday/last-minute)
- [ ] Stores detailed skip context
- [ ] No guilt-inducing language used

---

## Phase 6: Pattern Analysis & Adaptation (Day 5-6)

### Ticket 6.1: Day 7 Pattern Discovery
**Priority:** High
**Estimated Time:** 4 hours

**Tasks:**
- Aggregate Week 1 data for analysis
- Send comprehensive context to Claude
- Parse pattern analysis response
- Format and send multi-message analysis

**Acceptance Criteria:**
- [ ] Triggers automatically after Day 7 evening check-in
- [ ] Identifies 3-5 patterns with evidence
- [ ] Sends analysis in 5-7 digestible messages
- [ ] Saves patterns to pattern_analyses table
- [ ] User receives clear insights about their behavior

**Claude Prompt Structure:**
```python
def build_analysis_prompt(week_data: list) -> str:
    # Include all check-ins, skips, confidence scores
    # Request pattern identification with evidence
    # Ask for specific Week 2 adaptations
```

---

### Ticket 6.2: Week 2 Adaptive Planning
**Priority:** High
**Estimated Time:** 3 hours

**Tasks:**
- Generate Week 2 plan based on patterns
- Implement adaptive interventions
- Add night-before commitment flow
- Create "Lite" workout options

**Acceptance Criteria:**
- [ ] Week 2 plan addresses discovered patterns
- [ ] Includes 12-minute "Lite" alternatives
- [ ] Sunday 9pm commitment request scheduled
- [ ] Plan saved to workout_plans table
- [ ] User state transitions to week_2_active

---

### Ticket 6.3: Week 2 Night Commitment Feature
**Priority:** Medium
**Estimated Time:** 2 hours

**Tasks:**
- Schedule 9pm night-before check-ins
- Offer PRIMARY vs LITE choice
- Collect confidence score
- Compare to morning confidence

**Acceptance Criteria:**
- [ ] Asks for commitment night before
- [ ] Saves choice and confidence level
- [ ] Updates next day's planned workout
- [ ] Tracks if night confidence predicts completion

---

## Phase 7: Testing & Polish (Day 6-7)

### Ticket 7.1: End-to-End Testing
**Priority:** High
**Estimated Time:** 3 hours

**Tasks:**
- Test complete 14-day journey
- Verify all state transitions
- Test edge cases (missed check-ins, invalid inputs)
- Validate timezone handling

**Acceptance Criteria:**
- [ ] Can complete full onboarding flow
- [ ] Daily check-ins work for 7 consecutive days
- [ ] Pattern analysis generates successfully
- [ ] Week 2 begins with adaptations
- [ ] Messages arrive at correct times

---

### Ticket 7.2: Error Handling & Recovery
**Priority:** Medium
**Estimated Time:** 2 hours

**Tasks:**
- Add comprehensive error logging
- Implement graceful fallbacks
- Create admin alerts for critical failures
- Test recovery from crashes

**Acceptance Criteria:**
- [ ] All API failures handled gracefully
- [ ] Users receive helpful error messages
- [ ] System recovers from database outages
- [ ] Scheduled jobs resume after restart

---

### Ticket 7.3: Performance Optimization
**Priority:** Low
**Estimated Time:** 2 hours

**Tasks:**
- Add database query optimization
- Implement message batching
- Cache frequently accessed data
- Profile and optimize slow endpoints

**Acceptance Criteria:**
- [ ] Webhook responds in <5 seconds
- [ ] Can handle 20 concurrent users
- [ ] Database queries use proper indexes
- [ ] No memory leaks in scheduler

---

## Launch Checklist

### Pre-Launch (Day 7)
- [ ] All tickets completed and tested
- [ ] Production environment variables set
- [ ] Database backed up
- [ ] Twilio production number configured
- [ ] Error monitoring active
- [ ] Test with 2-3 internal users

### Launch Day (Day 8)
- [ ] Send onboarding link to 20 participants
- [ ] Monitor first interactions closely
- [ ] Check scheduler is creating jobs
- [ ] Verify morning check-ins scheduled
- [ ] Database writing correctly

### Daily Monitoring
- [ ] Check Railway logs for errors
- [ ] Verify scheduled messages sent
- [ ] Review completion rates
- [ ] Check Claude API usage
- [ ] Monitor database size

---

## Technical Debt & Future Improvements

### Post-MVP Enhancements
- Admin dashboard for monitoring users
- Bulk message sending optimization
- Advanced pattern analysis algorithms
- Exercise video integration
- Payment processing
- Multi-language support

### Known Limitations (Acceptable for MVP)
- Fixed timezone (London/Dublin only)
- No message queue (APScheduler only)
- Basic error reporting (logs only)
- Manual user management via database
- Single bot personality/tone

---

## Risk Mitigation

### High-Risk Areas
1. **Claude API Failures**
   - Mitigation: Retry logic + fallback templates

2. **Scheduler Crashes**
   - Mitigation: Job persistence + restart recovery

3. **Database Overload**
   - Mitigation: Connection pooling + query optimization

4. **Twilio Rate Limits**
   - Mitigation: Message queuing + rate limiting

5. **User Drops Out Mid-Experiment**
   - Mitigation: Gentle re-engagement + exit survey

---

## Definition of Done

A ticket is complete when:
1. Code is written and tested
2. Error handling implemented
3. Database migrations run successfully
4. Feature works end-to-end in production
5. Logs show successful execution
6. User receives expected messages

---

## Estimated Timeline

**Total Development Time:** 7-8 days

- Day 1: Project setup, deployment, database
- Day 2-3: Core messaging infrastructure
- Day 3-4: Onboarding flow
- Day 4-5: Daily check-in systems
- Day 5-6: Pattern analysis & adaptation
- Day 6-7: Testing & polish
- Day 8: Launch with first users

This plan delivers a minimal, elegant solution that focuses on core value: discovering why users fail and adapting to help them succeed.