function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", window.csrfToken);
        }
    }
});

function registerModalInit(options) {
    // options:
    // - nextUrl
    // - courseId

    var createUrl,
        updateUrl,
        loginUrl,
        containerFormZero,
        containerFormOne,
        containerFormTwoT,
        containerFormTwoS,
        containerFormThree,
        buttonInSaving,
        resetButton,
        validateForm,
        showFormErrors;

    $('.new-register').click(function(ev) {
        window.userType = $(this).data('user-type');
    });

    createUrl = "/labster/api/users/";
    loginUrl = "/labster/login-by-token/";
    updateUrl = function(userId) {
        return createUrl + userId + "/";
    };

    containerFormZero = $('.register-wizard-0');
    containerFormOne = $('.register-wizard-1');
    containerFormTwoT = $('.register-wizard-2-t');
    containerFormTwoS = $('.register-wizard-2-s');
    containerFormThree = $('.register-wizard-3');

    $('.button-link-submit').click(function(ev) {
        ev.preventDefault();
        $(this).closest('form').submit();
    });

    buttonInSaving = function(button) {
        button.data('original-html', button.html());
        button.html('<i class="icon fa fa-spinner fa-spin"></i> Saving');
    };

    resetButton = function(button) {
        button.html(button.data('original-html'));
    };

    validateForm = function(form) {
      var inputs,
          valid = true;

      form.find('.error-message').empty().hide();
      inputs = form.find('input.required,select.required');
      _.each(inputs, function(input) {
          var el = $(input);

          if (el.val().length == 0) {
              var errorMessage;
              if (input.tagName.toLowerCase() === 'select') {
                  errorMessage = el.closest('.select-container').siblings('.error-message');
              } else {
                  errorMessage = el.next('.error-message');
              }

              errorMessage.show().html('This field is required');
              valid = false;
          }
      });

      return valid;
    };

    showFormErrors = function(form, messages) {
        var getName,
            inputs;

        getName = function(name) {
            return "[name=" + name + "]";
        };

        _.each(messages, function(messageList, name) {
            inputs = form.find(getName(name));
            _.each(inputs, function(input) {
                _.each(messageList, function(message) {
                    if (message == "Email is used") {
                        message = 'Email already in use. Please <a href="/login">login here</a>.';
                    }
                    $(input).next('.error-message').append(message).show();
                });
            });
        });
    };

    containerFormZero.find('form').submit(function(ev) {
        var inputEmail,
            submit,
            email,
            erroMessage,
            form;

        form = containerFormZero.find('form');
        inputEmail = form.find('input[name=email]');
        submit = form.find('button[type=submit]');
        errorMessage = form.find('.error-message');

        email = inputEmail.val();

        buttonInSaving(submit);
        errorMessage.hide().empty();

        if (validateForm(form)) {
            $.ajax({
                url: createUrl,
                type: "POST",
                data: {email: email},
                success: function(response) {
                    window.user = response;
                    containerFormZero.fadeOut(function() {
                        containerFormOne.fadeIn();
                        containerFormThree.find('input[name=user_id]').val(window.user.id);
                        containerFormThree.find('input[name=token_key]').val(window.user.token_key);
                        containerFormThree.find('input[name=next]').val(options.nextUrl);
                        containerFormThree.find('input[name=course_id]').val(options.courseId);
                    });

                },
                error: function(obj, msg, status) {
                    var response = JSON.parse(obj.responseText);
                    showFormErrors(form, response);
                    resetButton(submit);
                }
            });
        } else {
            resetButton(submit);
        }

    return false;
    });

    containerFormOne.find('form').submit(function(ev) {
          var inputName,
              inputPassword,
              submit,
              name,
              password,
              form;

          form = containerFormOne.find('form');
          inputName = form.find('input[name=name]');
          inputPassword = form.find('input[name=password]');
          submit = form.find('button[type=submit]');

          name = inputName.val();
          password = inputPassword.val();

          buttonInSaving(submit);
          errorMessage.hide().empty();

          if (validateForm(form)) {
              $.ajax({
                  url: updateUrl(window.user.id),
                  type: "PUT",
                  data: {name: name, password: password, user_type: window.userType},
                  beforeSend: function(xhr, settings) {
                      xhr.setRequestHeader("Authorization", "Token " + window.user.token_key);
                  },
                  success: function(response) {
                      containerFormOne.fadeOut(function() {
                          if (parseInt(window.userType) === 2) {
                              containerFormTwoT.fadeIn();
                          } else {
                              containerFormTwoS.fadeIn();
                          }
                      });
                  },
                  error: function(obj, msg, status) {
                      resetButton(submit);
                  }
              });
          } else {
              resetButton(submit);
          }

          return false;
    });

    containerFormTwoT.find('form').submit(function(ev) {
          var inputUserSchoolLevel,
              inputOrganizationName,
              inputPhoneNumber,
              submit,
              userSchoolLevel,
              organizationName,
              phoneNumber,
              form,
              payload;

          form = containerFormTwoT.find('form');
          inputUserSchoolLevel = form.find('select[name=user_school_level]');
          inputOrganizationName = form.find('input[name=organization_name]');
          inputPhoneNumber = form.find('input[name=phone_number]');
          submit = form.find('button[type=submit]');

          userSchoolLevel = inputUserSchoolLevel.val();
          organizationName = inputOrganizationName.val();
          phoneNumber = inputPhoneNumber.val();

          buttonInSaving(submit);
          errorMessage.hide().empty();

          payload = {
              user_school_level: userSchoolLevel,
              organization_name: organizationName,
              phone_number: phoneNumber
          };

          if (validateForm(form)) {
              $.ajax({
                  url: updateUrl(window.user.id),
                  type: "PUT",
                  data: payload,
                  beforeSend: function(xhr, settings) {
                      xhr.setRequestHeader("Authorization", "Token " + window.user.token_key);
                  },
                  success: function(response) {
                      containerFormTwoT.fadeOut(function() {
                          containerFormThree.find('form').submit();
                      });
                  },
                  error: function(obj, msg, status) {
                      resetButton(submit);
                  }
              });
          } else {
              resetButton(submit);
          }

          return false;
    });

    containerFormTwoS.find('form').submit(function(ev) {
        var inputLevelOfEducation,
            inputGender,
            inputYearOfBirth,
            submit,
            levelOfEducation,
            gender,
            yearOfBirth,
            form,
            payload;

        form = containerFormTwoS.find('form');
        inputLevelOfEducation = form.find('select[name=level_of_education]');
        inputGender = form.find('select[name=gender]');
        inputYearOfBirth = form.find('select[name=year_of_birth]');
        submit = form.find('button[type=submit]');

        levelOfEducation = inputLevelOfEducation.val();
        gender = inputGender.val();
        yearOfBirth = inputYearOfBirth.val();

        buttonInSaving(submit);
        errorMessage.hide().empty();

        payload = {
            level_of_education: levelOfEducation,
            gender: gender,
            year_of_birth: yearOfBirth
        };

        if (validateForm(form)) {
            $.ajax({
                url: updateUrl(window.user.id),
                type: "PUT",
                data: payload,
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("Authorization", "Token " + window.user.token_key);
                },
                success: function(response) {
                    containerFormTwoS.fadeOut(function() {
                        containerFormThree.find('form').submit();
                    });
                },
                error: function(obj, msg, status) {
                    resetButton(submit);
                }
            });
        } else {
            resetButton(submit);
        }

        return false;
    });

}