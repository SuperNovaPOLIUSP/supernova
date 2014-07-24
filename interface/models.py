# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from __future__ import unicode_literals

from django.core import urlresolvers
from django.db import models


class Academicprogram(models.Model):
    idacademicprogram = models.IntegerField(db_column='idAcademicProgram', primary_key=True) # Field name made lowercase.
    name = models.CharField(max_length=255)
    vacancynumber = models.IntegerField(db_column='vacancyNumber', blank=True, null=True) # Field name made lowercase.
    abbreviation = models.CharField(max_length=45)
    startdate = models.DateField(db_column='startDate') # Field name made lowercase.
    enddate = models.DateField(db_column='endDate') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'academicProgram'

class AggrOffer(models.Model):
    idoffer = models.IntegerField(db_column='idOffer') # Field name made lowercase.
    idcourse = models.ForeignKey('Course', db_column='idCourse') # Field name made lowercase.
    idprofessor = models.ForeignKey('Professor', db_column='idProfessor') # Field name made lowercase.
    idtimeperiod = models.ForeignKey('Timeperiod', db_column='idTimePeriod') # Field name made lowercase.
    classnumber = models.IntegerField(db_column='classNumber') # Field name made lowercase.
    practical = models.IntegerField()
    numberofregistrations = models.IntegerField(db_column='numberOfRegistrations', blank=True, null=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'aggr_offer'

class AggrOpticalsheetfield(models.Model):
    idopticalsheetfield = models.IntegerField(db_column='idOpticalSheetField', primary_key=True) # Field name made lowercase.
    idopticalsheet = models.ForeignKey('Opticalsheet', db_column='idOpticalSheet') # Field name made lowercase.
    idoffer = models.ForeignKey(AggrOffer, db_column='idOffer') # Field name made lowercase.
    code = models.IntegerField(blank=True, null=True)
    courseindex = models.IntegerField(db_column='courseIndex', blank=True, null=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'aggr_opticalSheetField'

class AggrSurvey(models.Model):
    idsurvey = models.IntegerField(db_column='idSurvey') # Field name made lowercase.
    idopticalsheet = models.ForeignKey('Opticalsheet', db_column='idOpticalSheet') # Field name made lowercase.
    idquestionnaire = models.ForeignKey('Questionnaire', db_column='idQuestionnaire') # Field name made lowercase.
    assessmentnumber = models.IntegerField(db_column='assessmentNumber') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'aggr_survey'

class Alternativemeaning(models.Model):
    idalternativemeaning = models.IntegerField(db_column='idAlternativeMeaning', primary_key=True) # Field name made lowercase.
    idanswertype = models.ForeignKey('Answertype', db_column='idAnswerType') # Field name made lowercase.
    alternative = models.CharField(max_length=1)
    meaning = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'alternativeMeaning'

class Answer(models.Model):
    idanswer = models.IntegerField(db_column='idAnswer', primary_key=True) # Field name made lowercase.
    questionindex = models.IntegerField(db_column='questionIndex') # Field name made lowercase.
    iddatafile = models.ForeignKey('Datafile', db_column='idDatafile') # Field name made lowercase.
    alternative = models.CharField(max_length=1)
    identifier = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'answer'

class Answertype(models.Model):
    idanswertype = models.IntegerField(db_column='idAnswerType', primary_key=True) # Field name made lowercase.
    name = models.CharField(max_length=45)
    class Meta:
        managed = False
        db_table = 'answerType'

class Classrepresentative(models.Model):
    idclassrepresentative = models.IntegerField(db_column='idClassRepresentative', primary_key=True) # Field name made lowercase.
    name = models.CharField(max_length=255)
    memberid = models.IntegerField(db_column='memberId') # Field name made lowercase.
    email = models.CharField(max_length=255)
    cellphonenumber = models.IntegerField(db_column='cellphoneNumber', blank=True, null=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'classRepresentative'

class Course(models.Model):
    idcourse = models.IntegerField(db_column='idCourse', primary_key=True) # Field name made lowercase.
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=255)
    syllabus = models.TextField(blank=True)
    coursecode = models.CharField(db_column='courseCode', max_length=7) # Field name made lowercase.
    startdate = models.DateField(db_column='startDate') # Field name made lowercase.
    enddate = models.DateField(db_column='endDate') # Field name made lowercase.
    def get_absolute_url(self):
        return urlresolvers.reverse('interface:offer_edit', args=(self.pk,))
    class Meta:
        managed = False
        db_table = 'course'

class Coursecoordination(models.Model):
    idcoursecoordination = models.IntegerField(db_column='idCourseCoordination', primary_key=True) # Field name made lowercase.
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=45, blank=True)
    class Meta:
        managed = False
        db_table = 'courseCoordination'

class Cycle(models.Model):
    idcycle = models.IntegerField(db_column='idCycle', primary_key=True) # Field name made lowercase.
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=255)
    idcycletype = models.ForeignKey('Minitablecycletype', db_column='idCycleType') # Field name made lowercase.
    vacancynumber = models.IntegerField(db_column='vacancyNumber', blank=True, null=True) # Field name made lowercase.
    startdate = models.DateField(db_column='startDate') # Field name made lowercase.
    enddate = models.DateField(db_column='endDate') # Field name made lowercase.
    cyclecode = models.IntegerField(db_column='cycleCode') # Field name made lowercase.
    dayperiod = models.CharField(db_column='dayPeriod', max_length=45) # Field name made lowercase.
    termlength = models.ForeignKey('Minitablelength', db_column='termLength') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'cycle'

class Dataanalysisreport(models.Model):
    iddataanalysisreport = models.IntegerField(db_column='idDataAnalysisReport') # Field name made lowercase.
    idoffer = models.ForeignKey(AggrOffer, db_column='idOffer') # Field name made lowercase.
    idclassrepresentative = models.ForeignKey(Classrepresentative, db_column='idClassRepresentative') # Field name made lowercase.
    dataanalysisreport = models.TextField(db_column='dataAnalysisReport') # Field name made lowercase.
    submissiontime = models.DateTimeField(db_column='submissionTime', blank=True, null=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'dataAnalysisReport'

class Datafile(models.Model):
    iddatafile = models.IntegerField(db_column='idDatafile', primary_key=True) # Field name made lowercase.
    filename = models.CharField(db_column='fileName', max_length=255) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'datafile'

class Department(models.Model):
    iddepartment = models.IntegerField(db_column='idDepartment', primary_key=True) # Field name made lowercase.
    name = models.CharField(max_length=100)
    departmentcode = models.CharField(db_column='departmentCode', max_length=3) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'department'

class Encoding(models.Model):
    idopticalsheet = models.ForeignKey('Opticalsheet', db_column='idOpticalSheet', primary_key=True) # Field name made lowercase.
    name = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = 'encoding'

class Faculty(models.Model):
    idfaculty = models.IntegerField(db_column='idFaculty', primary_key=True) # Field name made lowercase.
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=45)
    campus = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'faculty'

class Minitablecycletype(models.Model):
    idcycletype = models.IntegerField(db_column='idCycleType', primary_key=True) # Field name made lowercase.
    name = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = 'minitableCycleType'

class Minitabledayoftheweek(models.Model):
    iddayoftheweek = models.IntegerField(db_column='idDayOfTheWeek', primary_key=True) # Field name made lowercase.
    dayoftheweek = models.CharField(db_column='dayOfTheWeek', max_length=15) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'minitableDayOfTheWeek'

class Minitablelength(models.Model):
    idlength = models.IntegerField(db_column='idLength', primary_key=True) # Field name made lowercase.
    length = models.CharField(max_length=15)
    class Meta:
        managed = False
        db_table = 'minitableLength'

class Minitablerequirementtype(models.Model):
    idrequirementtype = models.IntegerField(db_column='idRequirementType', primary_key=True) # Field name made lowercase.
    name = models.CharField(max_length=45)
    class Meta:
        managed = False
        db_table = 'minitableRequirementType'

class Minitablerequisitiontype(models.Model):
    idrequisitiontype = models.IntegerField(db_column='idRequisitionType', primary_key=True) # Field name made lowercase.
    requisitiontype = models.CharField(db_column='requisitionType', max_length=45) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'minitableRequisitionType'

class Minitablesurveytype(models.Model):
    idsurveytype = models.IntegerField(db_column='idSurveyType', primary_key=True) # Field name made lowercase.
    typename = models.CharField(db_column='typeName', max_length=45) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'minitableSurveyType'

class Opticalsheet(models.Model):
    idopticalsheet = models.IntegerField(db_column='idOpticalSheet', primary_key=True) # Field name made lowercase.
    idsurveytype = models.ForeignKey(Minitablesurveytype, db_column='idSurveyType') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'opticalSheet'

class Professor(models.Model):
    idprofessor = models.AutoField(db_column='idProfessor', primary_key=True) # Field name made lowercase.
    memberid = models.IntegerField(db_column='memberId') # Field name made lowercase.
    name = models.CharField(max_length=255)
    office = models.CharField(max_length=45, null=True, blank=True)
    email = models.CharField(max_length=65, null=True, blank=True)
    phonenumber = models.IntegerField(db_column='phoneNumber', blank=True, null=True) # Field name made lowercase.
    cellphonenumber = models.IntegerField(db_column='cellphoneNumber', blank=True, null=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'professor'

class Question(models.Model):
    idquestion = models.IntegerField(db_column='idQuestion') # Field name made lowercase.
    idanswertype = models.ForeignKey(Answertype, db_column='idAnswerType') # Field name made lowercase.
    questionwording = models.TextField(db_column='questionWording') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'question'

class Questionnaire(models.Model):
    idquestionnaire = models.IntegerField(db_column='idQuestionnaire', primary_key=True) # Field name made lowercase.
    description = models.CharField(max_length=255)
    creationdate = models.DateField(db_column='creationDate') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'questionnaire'

class RelAcademicprogramCycle(models.Model):
    idacademicprogram = models.ForeignKey(Academicprogram, db_column='idAcademicProgram') # Field name made lowercase.
    idcycle = models.ForeignKey(Cycle, db_column='idCycle') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'rel_academicProgram_cycle'

class RelAnswerOpticalsheetfieldSurvey(models.Model):
    idanswer = models.ForeignKey(Answer, db_column='idAnswer') # Field name made lowercase.
    idopticalsheetfield = models.ForeignKey(AggrOpticalsheetfield, db_column='idOpticalSheetField') # Field name made lowercase.
    idsurvey = models.ForeignKey(AggrSurvey, db_column='idSurvey') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'rel_answer_opticalSheetField_survey'

class RelClassrepresentativeOpticalsheet(models.Model):
    idclassrepresentative = models.ForeignKey(Classrepresentative, db_column='idClassRepresentative') # Field name made lowercase.
    idopticalsheet = models.ForeignKey(Opticalsheet, db_column='idOpticalSheet') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'rel_classRepresentative_opticalSheet'

class RelCoursecoordinationCycle(models.Model):
    idcoursecoordination = models.ForeignKey(Coursecoordination, db_column='idCourseCoordination') # Field name made lowercase.
    idcycle = models.ForeignKey(Cycle, db_column='idCycle') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'rel_courseCoordination_cycle'

class RelCoursecoordinationFaculty(models.Model):
    idcoursecoordination = models.ForeignKey(Coursecoordination, db_column='idCourseCoordination') # Field name made lowercase.
    idfaculty = models.ForeignKey(Faculty, db_column='idFaculty') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'rel_courseCoordination_faculty'

class RelCourseCycle(models.Model):
    idcourse = models.ForeignKey(Course, db_column='idCourse') # Field name made lowercase.
    idcycle = models.ForeignKey(Cycle, db_column='idCycle') # Field name made lowercase.
    term = models.IntegerField()
    startdate = models.DateField(db_column='startDate') # Field name made lowercase.
    enddate = models.DateField(db_column='endDate') # Field name made lowercase.
    requisitiontype = models.ForeignKey(Minitablerequisitiontype, db_column='requisitionType', blank=True, null=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'rel_course_cycle'

class RelCourseCycleCourse(models.Model):
    idcycle = models.ForeignKey(Cycle, db_column='idCycle') # Field name made lowercase.
    idcourse = models.ForeignKey(Course, db_column='idCourse', related_name='idCourse_relCourseCycleCourse') # Field name made lowercase.
    idrequirement = models.ForeignKey(Course, db_column='idRequirement', related_name='idRequirement_relCourseCycleCourse') # Field name made lowercase.
    idrequirementtype = models.ForeignKey(Minitablerequirementtype, db_column='idRequirementType') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'rel_course_cycle_course'

class RelCycleOpticalsheet(models.Model):
    idopticalsheet = models.ForeignKey(Opticalsheet, db_column='idOpticalSheet') # Field name made lowercase.
    idcycle = models.ForeignKey(Cycle, db_column='idCycle') # Field name made lowercase.
    term = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'rel_cycle_opticalSheet'

class RelDepartmentProfessor(models.Model):
    idprofessor = models.ForeignKey(Professor, db_column='idProfessor') # Field name made lowercase.
    iddepartment = models.ForeignKey(Department, db_column='idDepartment') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'rel_department_professor'

class RelOfferSchedule(models.Model):
    idschedule = models.ForeignKey('Schedule', db_column='idSchedule') # Field name made lowercase.
    idoffer = models.ForeignKey(AggrOffer, db_column='idOffer') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'rel_offer_schedule'

class RelQuestionQuestionnaire(models.Model):
    idquestionnaire = models.ForeignKey(Questionnaire, db_column='idQuestionnaire') # Field name made lowercase.
    idquestion = models.ForeignKey(Question, db_column='idQuestion') # Field name made lowercase.
    questionindex = models.IntegerField(db_column='questionIndex') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'rel_question_questionnaire'

class Schedule(models.Model):
    idschedule = models.IntegerField(db_column='idSchedule', primary_key=True) # Field name made lowercase.
    iddayoftheweek = models.ForeignKey(Minitabledayoftheweek, db_column='idDayOfTheWeek') # Field name made lowercase.
    start = models.TimeField()
    end = models.TimeField()
    frequency = models.CharField(max_length=45)
    class Meta:
        managed = False
        db_table = 'schedule'

class Timeperiod(models.Model):
    idtimeperiod = models.IntegerField(db_column='idTimePeriod', primary_key=True) # Field name made lowercase.
    length = models.ForeignKey(Minitablelength, db_column='length')
    year = models.IntegerField()
    session = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'timePeriod'

