
(cl:in-package :asdf)

(defsystem "beginner_tutorials-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "IntWithHeader" :depends-on ("_package_IntWithHeader"))
    (:file "_package_IntWithHeader" :depends-on ("_package"))
  ))