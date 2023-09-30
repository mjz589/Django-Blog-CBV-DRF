## api-v1 views

# Registration view
from .RegistrationApiView import *

# Activation and Verification views
from .ActivationApiView import *
from .ActivationResendApiView import *

# Password views
from .ChangePasswordApiView import *
from .ResetPasswordApiView import *
from .ResetPasswordConfirmApiView import *
from .ResetPasswordTokenApiView import *

# Token views
from .CostumTokenObtainPairView import *
from .CustomAuthToken import *
from .CustomDiscardAuthToken import *

# Profile view
from .ProfileApiView import *
