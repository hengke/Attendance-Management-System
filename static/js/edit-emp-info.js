$(function () {/* 文档加载，执行一个函数*/
    console.log("dasdasdsadsa")
    $('#defaultForm')
        .bootstrapValidator({
            message: 'This value is not valid',
            feedbackIcons: {
                /*input状态样式图片*/
                // valid: 'glyphicon glyphicon-ok',
                // invalid: 'glyphicon glyphicon-remove',
                // validating: 'glyphicon glyphicon-refresh'
            },
            fields: {
                /*验证：规则*/
                full_name: {//验证input项：验证规则
                    message: 'The full name is not valid',
                    validators: {
                        notEmpty: {//非空验证：提示消息
                            message: '用户名不能为空'

                        },
                        stringLength: {
                            min: 1,
                            max: 20,
                            message: '用户名长度必须在1到20之间'
                        },
                        regexp: {
                            regexp: /^.+$/,
                            message: ''
                        }
                    }
                },
                emp_num: {
                    message: 'The employee number is not valid',
                    validators: {
                        notEmpty: {
                            message: '员工编号不能为空'
                        },
                        stringLength: {
                            min: 8,
                            max: 8,
                            message: '请输入8位员工编号（不足8位首位用0填充）'
                        },
                        threshold: 1, //有1字符以上才发送ajax请求，（input中输入一个字符，插件会向服务器发送一次，设置限制，1字符以上才开始）
                        remote: {//ajax验证。server result:{"valid",true or false} 向服务发送当前input name值，获得一个json数据。例表示正确：{"valid",true}
                            url: '/register/',//验证地址
                            message: '员工编号已存在',//提示消息
                            delay: 2000,//每输入一个字符，就发ajax请求，服务器压力还是太大，设置2秒发送一次ajax（默认输入一个字符，提交一次，服务器压力太大）
                            type: 'POST',//请求方式
                            /**自定义提交数据，默认值提交当前input value*/
                            data: function(t) {
                               return {
                                   emp_num_verify: $('[emp_num="emp_num"]').val()
                                   // whatever: $('[name="whateverNameAttributeInYourForm"]').val()
                               };
                            }

                        },
                        regexp: {
                            // regexp: /^(x?[0-9]){10}|([0-9]{11})$/,
                            regexp: /^([0-9]{8})$/,
                            message: '请输入正确的员工编号'
                        }
                    }
                },
                department: {//验证input项：验证规则
                    message: 'The department is not valid',
                    validators: {
                        notEmpty: {//非空验证：提示消息
                            message: '部门不能为空'
                        },
                    }
                },
                user_type: {//验证input项：验证规则
                    message: 'The user type is not valid',
                    validators: {
                        notEmpty: {//非空验证：提示消息
                            message: '职务不能为空'
                        },
                    }
                },
                gender: {//验证input项：验证规则
                    message: 'The gender is not valid',
                    validators: {
                        notEmpty: {//非空验证：提示消息
                            message: '请选择性别'
                        },
                    }
                },
                email: {
                    validators: {
                        notEmpty: {
                            message: '邮件不能为空'
                        },
                        emailAddress: {
                            message: '请输入正确的邮件地址如：123@qq.com'
                        }
                    }
                },
                cell_phone: {
                    message: 'The cell phone is not valid',
                    validators: {
                        notEmpty: {
                            message: '手机号码不能为空'
                        },
                        stringLength: {
                            min: 11,
                            max: 11,
                            message: '请输入11位手机号码'
                        },
                        regexp: {
                            regexp: /^1[3|5|8|9|6|7]{1}[0-9]{9}$/,
                            message: '请输入正确的手机号码'
                        }
                    }
                },
                 work_phone: {
                    message: 'The work phone is not valid',
                    validators: {
                        stringLength: {
                            min: 7,
                            max: 13,
                            message: '请输入办公电话号码'
                        },
                        regexp: {
                            regexp: /^(\d{2,5}-\d{7,8}|\d{7,8})$/,
                            message: '请输入正确的手机号码'
                        }
                    }
                },
            }
        })

        //自动触发表单验证
        .on('success.form.bv', function (e) {//点击提交之后
            // Prevent form submission
            e.preventDefault();

            // Get the form instance
            var $form = $(e.target);

            // Get the BootstrapValidator instance
            var bv = $form.data('bootstrapValidator');

            // Use Ajax to submit form data 提交至form标签中的action，result自定义
            $.post('/register_verify/', $form.serialize(), function (result) {
//do something...
                if(result == 'OK'){
                    alert("注册成功，请登录！")
                    window.location.href='/login/'
                }
            });
        });
});