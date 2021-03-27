
(cl:in-package :asdf)

(defsystem "beginner_tutorials-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :sensor_msgs-msg
)
  :components ((:file "_package")
    (:file "AI" :depends-on ("_package_AI"))
    (:file "_package_AI" :depends-on ("_package"))
  ))