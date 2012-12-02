---
layout: post
title: "Building CatechizeMe with Rubymotion: The Gems and Cocoapods"
category:
tags:
  - Rubymotion
  - Cocoapods
  - Ruby
  - Projects
  - Testflight
  - iOS
---

This is a brief write-up on on some of the gems and cocoapods I used to build the [catechizeMe iOS app](http://bit.ly/catechizeme_ios) for [catechizeMe.com](http://catechizeme.com) using [Rubymotion](http://www.rubymotion.com/).

## The Ruby Gems

The `Gemfile` for the project:

    source :rubygems

    gem 'bubble-wrap'
    gem 'cocoapods'
    gem 'motion-cocoapods'
    gem 'motion-testflight'
    gem 'ib'

There were not a lot of extra Ruby gems needed to put this together. The most useful were [bubble-wrap](http://bubblewrap.io/), with its simplification of many things in the iOS Framework, and [ib](https://github.com/yury/ib), which allowed me to use Interface Builder to layout the UI.

The other gems are fairly self explanatory.  [cocoapods](http://cocoapods.org/) and [motion-cocoapods](https://github.com/HipByte/motion-cocoapods) allowed me to choose from many existing Obj-C libraries and avoid re-inventing the wheel.  [motion-testflight](https://github.com/HipByte/motion-testflight) made it easy to upload test builds for beta testers to try builds of the app during development.  If you haven't had a chance to try out [TestFlight](http://www.testflightapp.com), you should definitely check it out.

### Including the Ruby Gems

Using [Bundler](gembundler.com) made it easy to manage the dependencies.  After creating the `Gemfile` and making sure that Bundler was installed, `gem install bundler`, I just needed to download and install all the Ruby gems with a `bundle install`.  I could also update the gems to the latest version with a `bundle update`.  It should be noted that [you can specify versions of gems in the `Gemfile`](http://robots.thoughtbot.com/post/35717411108/a-healthy-bundle) and you will probably want to do this to avoid getting updated gems that break something or change things underneath you.

To include the gems in the project, I just had to add a couple of lines to the `Rakefile`:

    $:.unshift('/Library/RubyMotion/lib')
    require 'motion/project'

    require 'bundler'
    Bundler.require
    ...

### Gotchas

Not all Rubygems will work for Rubymotion.  There is no `require` functionality in Rubymotion, so you will need to find gems that have been built to work with Rubymotion.

## The Cocoapods

There are a lot existing open source Obj-C libraries out there that can be included in iOS projects.  Fortunately, we can also leverage many of those via Cocoapods, which aims to be the package manager for Obj-C projects (think Bundler).  Normally, you would have a `Podfile`, but for Rubymotion projects with the `motion-cocoapod` gem, you add your Pod dependencies to your `Rakefile`:

    ...
    app.pods do
      pod 'ViewDeck'
      pod 'QuickDialog'
      pod 'JSONKit'
      pod 'CMPopTipView'
      pod 'ShareKit/Facebook'
      pod 'ShareKit/Twitter'
    end
    ...

Much like Bundler, you can specify specific versions to avoid the pods getting updated beneath you. The Pods are installed into your project `vendor/Pods` directory where you can look through all the source when you need.

Here is how each Pod was used:

* [ViewDeck](https://github.com/Inferis/ViewDeck): slide out a view from the left or right, similar to Facebook or Path apps.  Used to make navigating and searching questions easier.
* [QuickDialog](http://escoz.com/quickdialog): made the settings form slightly easier to build.  Documentation is weak and you will need to be comfortable spelunking.
* [JSONKit](https://github.com/johnezang/JSONKit):  even though `bubble-wrap` has helpers for parsing JSON, it relies on iOS 5 features.  If your project needs to support iOS 4.3+, you will need to use something like JSONKit.
* [CMPopTipView](https://github.com/chrismiles/CMPopTipView): A nice little tooltip library to make the tutorial and show off features when some first installs the app.
* [ShareKit](https://github.com/ShareKit/ShareKit): A swiss army knife of sharing content to a number of sites. I only needed Facebook and Twitter, but there are a bunch more that can be used.

### Gotchas

Adding new Pods, it may sometimes appear that the Pod isn't available or working.  I found that because some Pods affect the project `.pch` file, it is sometimes neccessary to `rake clean` to get things working again.

## Conclusion

It is easy enough to leverage the growing number of Rubymotion gems and Obj-C iOS libraries.  The challenge can be finding them so that you don't re-invent the wheel.
