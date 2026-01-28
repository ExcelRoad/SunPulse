from django.db import models

class CustomerType(models.TextChoices):
    PRIVATE = 'private', 'פרטי'
    BUSINESS = 'business', 'עסקי'


class LeadStatus(models.TextChoices):
    NEW = 'new', 'חדש'
    QUOTE = 'quote', 'הצעת מחיר'
    WON = 'won', 'הומר'
    LOST = 'lost', 'אבוד'


class ContractType(models.TextChoices):
    MONITORING = 'monitoring', 'ניטור'
    LEADS = 'leads', 'לידים'
    MAINTENANCE = 'maintenance', 'תחזוקה'


class ContractStatus(models.TextChoices):
    DRAFT = 'draft', 'טיוטה'
    SENT = 'sent', 'נשלח'
    APPROVED = 'approved', 'אושר'
    REVISE = 'revise', 'עבר גרסה'
    LOST = 'lost', 'אבוד'


class SyncStatus(models.TextChoices):
    OK = 'ok', 'תקין'
    ERROR = 'error', 'שגיאה'
    PENDING = 'pending', 'ממתין'


class AlertPriority(models.TextChoices):
    LOW = 'low', 'נמוכה'
    MEDIUM = 'medium', 'בינונית'
    HIGH = 'high', 'גבוהה'
    CRITICAL = 'critical', 'קריטי'


class AlertStatus(models.TextChoices):
    NEW = 'new', 'חדשה'
    ACKNOWLEDGE = 'acknowledge', 'אושרה'
    IN_PROGRESS = 'in_progress', 'בטיפול'
    RESOLVED = 'resolved', 'נפתרה'
    CLOSED = 'closed', 'נסגרה'


class TicketStatus(models.TextChoices):
    OPEN = 'open', 'פתוח'
    IN_PROGRESS = 'in_progress', 'בטיפול'
    WAITING = 'waiting', 'ממתין'
    RESOLVED = 'resolved', 'נפתר'
    CLOSED = 'closed', 'נסגר'


class UserRole(models.TextChoices):
    ADMIN = 'admin', 'אדמין'
    ANALYST = 'analyst', 'אנליסט'
    VIEWER = 'viewer', 'צופה'