fetch("/api/category_courses/development/1").then((response)=>{return response.json()}).then((user)=>{
    console.log(user.objects[0][0].category__name + "_row");
    if  (document.getElementById(user.objects[0][0].category__name + "_row")){
        for(var i;i<user.objects.length;i++){

            document.getElementById(user.objects[i][0].category__name + "_row").innerHTML = `
                                ${user.objects[i].map(function(course){
                                    return `
                                    ${course.category__name}
                                    <div id="each-course-model" class="course-block col-lg-3 col-md-4 col-sm-12">
                                    <div class="inner-box">
                                        <div class="image">
                                            <a href="course-lesson.html"><img src="/media/${course.img_main}" alt="" /></a>
                                            <div class="time">15 horas</div>
                                        </div>
                                        <div class="lower-content">
                                            <h6><a href="course-lesson.html">${course.title}</a></h6>
                                            <ul class="post-meta">
                                                
                                            </ul>
                                            <div class="clearfix">
                                                <div class="pull-left">
                                                    <div class="author">Por: <span>${course.instructor__user__first_name} ${course.instructor__user__last_name}</span></div>
                                                </div>
                                                <div class="pull-right">
                                                    <div class="price">$</div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>`
                                }).join("")}
                                
                `
        }
    }

})