

# Clean Job Titles
IT['job_title'] = IT['Job Title'].str.strip()
IT['job_title'] = IT['job_title'].str.lower()

dic = {
    ('php developer', 'php web developer', 'magento developer', 'senior php developer', 'php developers', 'php developer','sr. php developer'): 'php developer', 
    ('senior software engineer', 'software engineer 2', 'sr. software engineer', 'delv senior software eng', 'sharepoint developer', 'senior software engg = systems', 'software development engineer', 'software engineer', 'sr software engineer', 'principal software engineer', 'software engineering', 'senior software engineer - java',  'software architect','delv software engineer', 'senior software engineer'): 'software engineer', 
    # 'embedded developer','embedded software engineers',
    ('angular developer', 'ios developer', 'mobile developer', 'ios developer', 'mobile application developer', 'application developer', 'ios developer', 'senior android developer', 'android developer', 'iphone developer','mobile app developer'): 'application developer', 
    ('java developer', 'java developer', 'java enterprise edition', 'senior java developer', 'core java developer', 'java developers', 'sr. java developer'): 'application developer',#'java developer', 
    ('dot net developers', '.net developer', 'core java developer', 'asp.net developer', ' senior .net developer', 'asp.net developer', 'net developer', 'dot net developer','senior .net developer','asp .net developer','dotnet developer'): 'application developer',#'dot net developer', 
    ('analyst', 'business analyst', 'senior business analyst'): 'business analyst', 
    ('web designer', 'wordpress developer', 'html developer', 'web developer'): 'web developer', 
    ('software developer', 'senior software developer'): 'software developer', 
    ('full stack developer', 'java full stack developer', 'senior full stack developer'): 'full stack developer', 
    ('python developer','python'): 'python developer', 
    ('ui ux designer', 'senior ui developer', 'ui developer', 'ux designer', 'ui / ux designers'): 'ui/ux developer', 
    ('program manager', 'project manager', 'technical product manager', 'product manager', 'technical project manager', 'assistant manager', 'manager'): 'manager', 
    ('job description', 'content writer', 'delivery module lead', 'informatica developer','writer','job description'): 'na', 
    ('front end developer','frontend developer','front end dev','frontend dev'): 'front end developer', 
    ('backend developer','back end developer','back end dev','backend dev'): 'backend developer', 
    ('senior devops engineer', 'devops engineer'): 'devops engineer', 
    ('technical  lead', 'team leader', 'tech lead','tech lead'): 'lead', 
    ('consultant', 'associate consultant', 'functional consultant', 'sap abap consultant'): 'consultant', 
    ('seo executive', 'seo'): 'seo', 
    ('automation test engineer', 'qa engineer', 'quality assurance engineer', 'test engineer', 'automation engineer', 'software automation test engineer','test engineer'): 'quality assurance engineer', 
    ('network engineer','net engineer'): 'network engineer', 
    ('data engineer', 'sql developer', 'big data developer', 'big data engineer'): 'data engineer', 
    ('data scientist','data scientist'): 'data scientist', 
    ('senior programmer','senior programmer'): 'senior programmer', 
    ('solution architect','solution architect'): 'solution architect',
    ('c++ developer','c++ developer'): 'c++ developer',
    ('front end developer', 'front end developer', 'front-end developer'): 'frontend developer'
    
}
dic2 = {
    ('php developer', 'php web developer', 'magento developer', 'senior php developer', 'php developers', 'php developer','sr. php developer','technical lead - php'): 'php developer', 
    ('senior software engineer', 'software engineer 2', 'sr. software engineer', 'delv senior software eng', 'sharepoint developer', 'senior software engg = systems', 'software development engineer', 'software engineer', 'sr software engineer', 'principal software engineer', 'software engineering', 'senior software engineer - java',  'software architect','delv software engineer', 'senior software engineer'): 'software engineer', 
    ('angular developer', 'ios developer', 'mobile developer', 'ios','ios developer', 'mobile application developer', 'application developer', 'ios developer', 'senior android developer', 'android developer', 'iphone developer','mobile app developer'): 'application developer', 
    ('java developer', 'java developer', 'java enterprise edition', 'senior java developer', 'core java developer', 'java developers', 'sr. java developer'): 'application developer',
    ('dot net developers', '.net developer', 'core java developer', 'asp.net developer', ' senior .net developer', 'asp.net developer', 'net developer', 'dot net developer','senior .net developer','asp .net developer','dotnet developer'): 'application developer',
    ('analyst', 'business analyst', 'senior business analyst'): 'business analyst',
    ('web designer', 'wordpress developer', 'html developer', 'web developer'): 'web developer', 
    ('software developer', 'senior software developer'): 'software developer', 
    ('full stack developer', 'java full stack developer', 'senior full stack developer','cloud product - full stack (react with node js) -zen3- hyd / vizag'): 'full stack developer', 
    ('python developer','python'): 'python developer', 
    ('ui ux designer', 'senior ui developer', 'ui developer', 'ux designer', 'ui / ux designers'): 'ui/ux developer', 
    ('program manager', 'project manager', 'technical product manager', 'product manager', 'technical project manager', 'assistant manager', 'manager'): 'manager', 
    ('job description', 'content writer', 'delivery module lead', 'informatica developer','writer','job description'): 'NaN', 
    ('front end developer','frontend developer','front end dev','frontend dev','front end developer', 'front end developer', 'front-end developer'): 'front end developer', 
    ('backend developer','back end developer','back end dev','backend dev'): 'backend developer', 
    ('senior devops engineer', 'devops engineer'): 'devops engineer', 
    ('technical  lead', 'team leader', 'tech lead','tech lead'): 'lead', 
    ('consultant', 'associate consultant', 'functional consultant', 'sap abap consultant'): 'consultant', 
    ('seo executive', 'seo'): 'seo', 
    ('automation test engineer', 'qa engineer', 'quality assurance engineer', 'test engineer', 'automation engineer', 'software automation test engineer','test engineer'): 'quality assurance engineer', 
    ('network engineer','net engineer'): 'network engineer', 
    ('data engineer', 'sql developer', 'big data developer', 'big data engineer'): 'data engineer', 
    ('data scientist','data scientist'): 'data scientist', 
    ('senior programmer','senior programmer'): 'senior programmer', 
    ('solution architect','solution architect'): 'solution architect',
    ('c++ developer','c++ developer'): 'c++ developer',
    ('front end developer', 'front end developer', 'front-end developer'): 'frontend developer',
    # Add the new mappings here
    ('quality assurance lead', 'quality assurance lead - regression/automation testing','technical test lead - ev'): 'quality assurance engineer',
    ('java devops lead', 'java development architect', 'java devops lead'): 'application developer',#'java developer',
    ('dot net development executive', 'dotnet developer', '.net developer'): 'application developer',#'dot net developer',
    ('salesforce developer','senior salesforce developer - apex/ visual force'):'salesforce developer',
    ('we are hiring for security engineer- microsoft 365',):'security engineer',
    ('java development architect', 'j2ee practice lead', 'it helpdesk technician - 3rd party payrole',  
     'sdn / nfv engineer', 'hiring cloud support associate for largest cloud computing company', 'technical support l1', 
     'atcatac engineer', 'sap hana architect', 'senior java architect', 'principal , project / program management', 
     'lead dlp specialist / implementor', 'rsystems is hiring for c++ with webrtc noida', 'service reliability engineer', 
     'urgent opening for sap bw/hana for noida', 'technical solutions engineer, google cloud (apigee)', 'cisco certification trainer', 
      'opening for system admin in a well known it company @ sakinaka(mumbai)', 
     'elixir developer', 'verification enginer / verfication lead', 'react.js developer - javascript/flux/redux', 
     'expert / lead-soc design engineer', 'vision plus',  
     'linux system administratorexpertise in conf', 'guidewire test lead',  
     'sap hr and success factors- employee central', 'ibm integration bus lead',  
     'windows support executive min 6 month experience',  
     'model based developer', 'business expert', 'engineer network services - data', 'jr. customer service executive-telecom network operation', 
     'linux kernel firmware developers', 'hiring for snowflake cloud datawarehouse', 'embedded device driver developer', 
     'avp - it application engineer', 'speech engineer', 'sap sd- 5+ yrs - bangalore - c2h',  
     'nodejs and ionic web ninja in an established and invested startup', 'bmc service request management copy 2', 
     'saas bi administrator', 'software system testing for mnc spaze it park sohna road gurgaon'): 'Other',
}

role_dic = {
 'Testing Engineer': 'quality assurance engineer', # 56% qa engineer, 16% BusAna, ..., possible all to Quality Assurance
 'Webmaster': 'web developer', # Web Developer # 70% is seo, 2% BusAna diverse, so choosing between Web Dev or SEO
 'Software Developer': 'NaN', # 33% App Dev, 19% software engineer, I think we should label this with the job_title_dic_sub instead # first label where job_title_dic are application developer
 'DBA': 'database administrator', # 105, diverse, Database Administrator
 'Technical Writer': 'technical writer', # 32, 90% is NA, lets just say its a technical writer
 'IT/Networking-Manager': 'NaN', # Networking Manager # 63, 63% is manager, BusAna, softwareeng, python eng, network eng, diverse, use job_title_dic_sub
 #!! bet lets make the manager here to be a network manager, then use job_title_dic_sub
 'Business Analyst': 'business analyst', # 83% is Business Analyst so I am going to keep it in that way
 'Graphic/Web Designer': 'NaN', # 58% is Web Developer, 24% UI/UX developer, diverse, 
 # web dev, ui dev, graphic des, ui des, php, rest is web des or just all of them is same
 'Quality Assurance/Quality Control Executive': 'NaN', 
  # 45% Quality Assurance Engineer, 22% Business Analyst, then rest is quality assurance engineer
 'Team Lead/Technical Lead': 'team/technical lead', # lead, manager, consultant, etc but still they are a Lead, use either team or technical or diff
 'Project Manager-IT/Software': 'project manager', # 87% Project Manager
 'Fresher': 'NaN', 
  # I think we should label this with the job_title_dic_sub instead
 'Outside Technical Consultant': 'consultant', # consultant
 'Technical Architect': 'NaN', 
    # 355, diverse, can use the job_title_dic_sub
 'System Analyst': 'NaN', # 67% Bussiness Analyst or can be replace to Data Analyst
    # nan, use bussiness analyst from job_title hen rest is system analyst
 'Technical Support Engineer': 'NaN',  # 204 diversed, maybe need to use the job_title_dic_sub
    # use the rest that are on job_title then what is left is labled to technical support engineer
 'Outside Consultant': 'consultant', # consultant
 'Functional Outside Consultant': 'consultant', # consultant
 'ERP Consultant': 'NaN', # remove
 'Release Manager': 'release manager', # 8 manager 1 devops engineer, 
 'Project Lead': 'project lead', # 37% Manager, 10% (4) consultant, diverse
 'Network Administrator': 'network administrator', # network admin
 'System Administrator': 'NaN', # 20% is devops engineer, 15% system admin, 9% consultant, diverse
    # use job_title then rest is system admin
 'Network Planning Engineer': 'network engineer', #NETWORK ENGINEER
 'Program Manager': 'program manager', # 78% manager, diverse, but lets keep it as it is
 'IT/Technical Content Developer': 'technical content developer', # 32% na, app dev 18% diverse
 'Trainee': 'trainee', # I think we should label this with the job_title_dic_sub instead
 'Product Manager': 'product manager',# 99 same
 'Quality Assurance/Quality Control Manager': 'quality assurance engineer', # 18, Quality Assurance Engineer
 'Technical Support Manager': 'support engineer', # 33% (7) manager, diverse, can be support engineer
 'Subject Matter Expert': 'subject matter expert', # 18, diverse, etc, lets keep it
 'Solution Architect / Enterprise Architect': 'solution/enterprise architect', # 43, 57% is solution architect, diverse, so lets say its same 
 'System Security': 'system security', # same
 'Customer Support Engineer/Technician': 'support engineer/technician', # Support Engineer/Technician
 'Head/VP/GM-Technology(IT)/CTO': 'head/vp/gm-technology/cto', # 80, 25% is manager, chief tech officer 12% (3), diverse, lets keep this but change name
 'Database Architect/Designer': 'database architect/designer', # 67, Data Engineer or keep the same 
 'Trainer/Faculty': 'trainer/faculty', # keep the same
 'EDP Analyst': 'NaN', #remove
 'Datawarehousing Technician': 'NaN', # Data Sciencetist/ Consultant 1:1
 'Practice Head / Practice Manager': 'NaN', # 17, diverse
 'Head/VP/GM-Quality': 'NaN', # 15, 20% consultant, diverse, else left with 1 or 6%
 'System Integration Technician': 'NaN', #consultant/other 1:1
 'Maintenance Engineer': 'NaN', #remove
 'Hardware Design Engineer': 'hardware engineer', # 23, hardware engineer 
 'Management Information Systems(MIS)-Manager': 'manager' # manager?
}
# missing Instructional Designer (9)
# 6-2 should not use the same, their roles and job title are mixed, then 1 is lacking data too, so lets remove this guys






IT_subset['Skills'] = IT_subset['Key Skills'].apply(lambda x: x.split('|'))
IT_subset['Skills'] = IT_subset['Skills'].apply(lambda x: [item.strip() for item in x])
IT_subset['Skills'] = IT_subset['Skills'].apply(lambda x: list(set([item.lower() for item in x])))
IT_subset.head()